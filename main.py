from fastapi import FastAPI, HTTPException, status
from uuid import UUID
from pydantic import BaseModel, Field
from enum import Enum



WALLETS = {
	UUID('123e4567-e89b-43d3-a456-426614174000'): 1000
}


class OperationType(str, Enum):
	DEPOSIT = "DEPOSIT"
	WITHDRAW = "WITHDRAW"


class Operation(BaseModel):
	operation_type: OperationType
	amount: int = Field(gt=0)


# что должен отдать get
class WalletResponse(BaseModel):
	wallet_id: UUID
	balance: int


# что должен отдать post
class OperationResponse(BaseModel):
	wallet_id: UUID
	balance: int


app = FastAPI()


@app.get(
	"/api/v1/wallets/{wallet_uuid}",
	response_model=WalletResponse,
	tags=["Информация о балансе кошелька"]
)
def get_wallet_balance(wallet_uuid: UUID) -> dict:
	try:
		return {
			'wallet_id': wallet_uuid,
			'balance': WALLETS[wallet_uuid]
		}
	except KeyError:
		raise HTTPException(detail=f'Кошелек {wallet_uuid} не найден!',
		                    status_code=status.HTTP_404_NOT_FOUND)


@app.post(
	"/api/v1/wallets/{wallet_uuid}/operation",
	response_model=OperationResponse,
	tags=['Операции с кошельком']
)
def create_wallet_operation(wallet_uuid: UUID, operation: Operation) -> dict:
	if wallet_uuid not in WALLETS:
		raise HTTPException(detail=f'Кошелек {wallet_uuid} не найден!',
		                    status_code=status.HTTP_404_NOT_FOUND)

	if operation.operation_type == OperationType.DEPOSIT:
		WALLETS[wallet_uuid] += operation.amount
		return {
			'wallet_id': wallet_uuid,
			'balance': WALLETS[wallet_uuid]
		}

	elif operation.operation_type == OperationType.WITHDRAW:
		if operation.amount > WALLETS[wallet_uuid]:
			raise HTTPException(detail=f"Недостаточно средств на счёте", status_code=status.HTTP_400_BAD_REQUEST)
		WALLETS[wallet_uuid] -= operation.amount
		return {
			'wallet_id': wallet_uuid,
			'balance': WALLETS[wallet_uuid]
		}