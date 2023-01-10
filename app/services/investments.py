from sqlalchemy import asc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.services.investment_logic import donation_investment, project_input


async def get_objects(
        objects_to_get,
        session: AsyncSession
):
    """Общая функция для получения необходимых объектов -
    проектов или пожертвований."""
    not_closed_objects = await session.execute(
        select(objects_to_get).where(
            objects_to_get.fully_invested == '0'
        ).order_by(asc(objects_to_get.create_date)))

    return not_closed_objects


async def distribute_new_donation(
        donation: Donation,
        session: AsyncSession
):
    """Передача в незакрытые проекты пожертвования
    в момент его создания."""
    not_closed_projects_objects = await get_objects(CharityProject, session)
    not_closed_projects = not_closed_projects_objects.scalars().all()

    donation = donation_investment(donation, not_closed_projects)

    session.add(donation)
    await session.commit()
    await session.refresh(donation)

    return donation


async def send_money_to_new_project(
        project: CharityProject,
        session: AsyncSession
):
    """Передача имеющихся пожертвований в новый проект
    в момент его создания."""
    not_closed_donations_objects = await get_objects(Donation, session)
    not_closed_donations = not_closed_donations_objects.scalars().all()

    project = project_input(project, not_closed_donations)

    session.add(project)
    await session.commit()
    await session.refresh(project)

    return project
