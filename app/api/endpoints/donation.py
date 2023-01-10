from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user, User
from app.crud.donation import donation_crud
from app.schemas.donation import DonationCreate, DonationDB, PartialDonation
from app.services.investments import distribute_new_donation

router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/my',
    response_model=List[PartialDonation],
    response_model_exclude={'user_id'}
)
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    donations = await donation_crud.get_donations_by_user_id(user, session)
    return donations


@router.post(
    '/',
    response_model=PartialDonation,
    response_model_exclude_none=True
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    donation = await donation_crud.create(donation, session, user)
    await distribute_new_donation(donation, session)
    return donation
