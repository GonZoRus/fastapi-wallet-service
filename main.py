from fastapi import FastAPI
from uuid import UUID
from pydantic import BaseModel, Field
from enum import Enum


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
	operation_type: OperationType
	amount: int


app = FastAPI()


@app.get(
	"/api/v1/wallets/{wallet_uuid}",
	response_model=WalletResponse,
	tags=["Информация о кошельке"]
)
def get_wallet_balance(wallet_uuid: UUID) -> dict:
	return {
		"wallet_id": wallet_uuid,
		"balance": 1000
	}


@app.post(
	"/api/v1/wallets/{wallet_uuid}/operation",
	response_model=OperationResponse,
	tags=['Операции с кошельком']
)
def create_wallet_operation(wallet_uuid: UUID, operation: Operation) -> dict:
	return {
		"wallet_id": wallet_uuid,
		'operation_type': operation.operation_type,
		'amount': operation.amount,
	}
