from fastapi import HTTPException
from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def check_project_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_charity_project_id_by_name(
        project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_if_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession
) -> CharityProject:
    """Проверка - существует ли благотворительный проект
    с указанным id."""
    project_to_check = await charity_project_crud.get(charity_project_id, session)
    if not project_to_check:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Благотворительный проект не найден!'
        )
    return project_to_check


async def check_if_there_is_money_in_project(
        charity_project_id: int,
        session: AsyncSession
) -> CharityProject:
    project_to_check = await charity_project_crud.get(charity_project_id, session)
    if project_to_check.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return project_to_check


async def check_if_invested_gt_full(
        project_to_update: CharityProject,
        incoming_data,
) -> CharityProject:
    """Запрет на установление полной суммы проекта в размере меньшем,
    чем уже было внесено."""
    if incoming_data.full_amount < project_to_update.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Недопустимо устанавливать максимальную сумму инвестиций проекта '
                   'меньше, чем уже фактически внесено денег'

        )
    return project_to_update


async def check_if_project_is_closed(
        project_in: CharityProject,
):
    if project_in.fully_invested is True:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
