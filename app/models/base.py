from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base


class CharityDonationBase(Base):
    # Абстрактная модель
    __abstract__ = True
    __table_args__ = (
        CheckConstraint('full_amount > 0'),
        CheckConstraint('invested_amount >= 0'),
        CheckConstraint('invested_amount <= full_amount'),
    )

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    def __repr__(self) -> str:
        return (
            f'full_amount: {self.full_amount}, '
            f'invested_amount: {self.invested_amount}, '
            f'fully_invested: {self.fully_invested}, '
            f'create_date: {self.create_date}, '
            f'close_date: {self.close_date}'
        )
