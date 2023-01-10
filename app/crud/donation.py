from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.models.user import User


# Создаем новый класс, унаследованный от CRUDBase.
class DonationCRUD(CRUDBase):

    async def get_donations_by_user_id(
            self,
            user: User,
            session: AsyncSession):
        donation = await session.execute(
            select(Donation).where(Donation.user_id == user.id))

        return donation.scalars().all()


donation_crud = DonationCRUD(Donation)
