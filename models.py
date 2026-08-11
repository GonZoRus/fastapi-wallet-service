from uuid import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
	...


class Wallet(Base):
	__tablename__ = 'wallets'
	wallet_uuid: Mapped[UUID] = mapped_column(primary_key=True)
	balance: Mapped[int]
