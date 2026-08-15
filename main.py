import logging
from enum import Enum
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from logging_config import configure_logging
from models import Wallet

configure_logging()
logger = logging.getLogger(__name__)


class OperationType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class Operation(BaseModel):
    operation_type: OperationType
    amount: int = Field(gt=0)



class WalletResponse(BaseModel):
    wallet_uuid: UUID
    balance: int



class OperationResponse(BaseModel):
    wallet_uuid: UUID
    balance: int


app = FastAPI()


@app.get(
    "/api/v1/wallets/{wallet_uuid}",
    response_model=WalletResponse,
    tags=["Информация о балансе кошелька"],
)
async def get_wallet_balance(
    wallet_uuid: UUID,
    session: AsyncSession = Depends(get_session),  # noqa: B008
):
    query = select(Wallet).where(Wallet.wallet_uuid == wallet_uuid)
    result = await session.execute(query)
    wallet: Wallet | None = result.scalar_one_or_none()

    if wallet is None:
        logger.warning(f"Кошелёк {wallet_uuid} не найден")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"В базе нет кошелька с {wallet_uuid}",
        )

    logger.info(f"Кошелек {wallet_uuid} найден, данные получены")
    return {"wallet_uuid": wallet.wallet_uuid, "balance": wallet.balance}


@app.post(
    "/api/v1/wallets/{wallet_uuid}/operation",
    response_model=OperationResponse,
    tags=["Операции с кошельком"],
)
async def create_wallet_operation(
    wallet_uuid: UUID,
    operation: Operation,
    session: AsyncSession = Depends(get_session),  # noqa: B008
):
    query = select(Wallet).where(Wallet.wallet_uuid == wallet_uuid).with_for_update()
    result = await session.execute(query)
    wallet: Wallet | None = result.scalar_one_or_none()

    if wallet is None:
        logger.warning(f"Кошелёк {wallet_uuid} не найден")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"В базе нет кошелька с {wallet_uuid}",
        )

    if operation.operation_type == OperationType.DEPOSIT:
        wallet.balance += operation.amount
        await session.commit()
        logger.info(f"Кошелек {wallet_uuid} пополнен на {operation.amount}")
        return {"wallet_uuid": wallet.wallet_uuid, "balance": wallet.balance}

    if operation.operation_type == OperationType.WITHDRAW:
        if operation.amount > wallet.balance:
            logger.warning(
                f"Недостаточно средств на кошельке {wallet_uuid}: "
                f"запрошено {operation.amount}, доступно {wallet.balance}"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Недостаточно средств на счёте",
            )

        wallet.balance -= operation.amount
        await session.commit()
        logger.info(f"Со счета кошелька {wallet_uuid} списано: {operation.amount}")
        return {"wallet_uuid": wallet.wallet_uuid, "balance": wallet.balance}
