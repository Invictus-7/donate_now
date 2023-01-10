from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.investments import send_money_to_new_project
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectUpdate, CharityProjectDB
)

from .validators import (check_if_charity_project_exists,
                         check_if_there_is_money_in_project,
                         check_project_name_duplicate,
                         check_if_invested_gt_full,
                         check_if_project_is_closed)

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session)
):
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Создание благотворительного проекта.
    Только для суперпользователей."""
    await check_project_name_duplicate(charity_project.name, session)
    new_charity = await charity_project_crud.create(charity_project, session)
    # Вытягиваем деньги из "висевших" на момент создания проекта донатов
    await send_money_to_new_project(new_charity, session)
    return new_charity


@router.patch(
    '/{project_id}',
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    project_to_update = await check_if_charity_project_exists(project_id, session)
    # Проверка уникальности имени объекта
    if obj_in.name is not None:
        await check_project_name_duplicate(obj_in.name, session)
    # Проверка, не закрыт ли вообще проект
    await check_if_project_is_closed(project_to_update)
    # Сравнение обновляемой требуемой суммы и фактически инвестированной суммы
    if obj_in.full_amount is not None:
        await check_if_invested_gt_full(project_to_update, obj_in)
    # Вызов метода для обновления проекта
    updated_project = await charity_project_crud.update(project_to_update, obj_in, session)
    return updated_project


@router.delete(
    '/{project_id}',
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Удаление благотворительного проекта.
    Только для суперпользователей."""
    charity_project = await check_if_charity_project_exists(project_id, session)
    await check_if_there_is_money_in_project(project_id, session)
    charity_project = await charity_project_crud.remove(charity_project, session)
    return charity_project
