
import asyncio

import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.mark.asyncio(loop_scope='session')
async def test_get_wallet(test_wallet):
	transport = ASGITransport(app=app)
	base_url = "http://test"
	async with AsyncClient(transport=transport, base_url=base_url) as client:
		response = await client.get(f"/api/v1/wallets/{test_wallet.wallet_uuid}")
		assert response.status_code == 200
		assert response.json()['wallet_uuid'] == str(test_wallet.wallet_uuid)
		assert response.json()['balance'] == test_wallet.balance


@pytest.mark.asyncio(loop_scope='session')
async def test_get_wallet_not_found():
	transport = ASGITransport(app=app)
	base_url = "http://test"
	async with AsyncClient(transport=transport, base_url=base_url) as client:
		response = await client.get("/api/v1/wallets/123e4567-e89b-43d3-a456-426614174003")
		assert response.status_code == 404


@pytest.mark.asyncio(loop_scope='session')
async def test_deposit(test_wallet):
	transport = ASGITransport(app=app)
	base_url = "http://test"
	async with AsyncClient(transport=transport, base_url=base_url) as client:
		response = await client.post(
			f"/api/v1/wallets/{test_wallet.wallet_uuid}/operation",
			json={
				"operation_type": "DEPOSIT",
				"amount": 400,
			}
		)
		assert response.status_code == 200
		assert response.json()['wallet_uuid'] == str(test_wallet.wallet_uuid)
		assert response.json()['balance'] == 1000


@pytest.mark.asyncio(loop_scope='session')
async def test_withdraw(test_wallet):
	transport = ASGITransport(app=app)
	base_url = "http://test"
	async with AsyncClient(transport=transport, base_url=base_url) as client:
		response = await client.post(
			f"/api/v1/wallets/{test_wallet.wallet_uuid}/operation",
			json={
				"operation_type": "WITHDRAW",
				"amount": 200,
			})
		assert response.status_code == 200
		assert response.json()['wallet_uuid'] == str(test_wallet.wallet_uuid)
		assert response.json()['balance'] == 400


@pytest.mark.asyncio(loop_scope='session')
async def test_withdraw_not_found():
	transport = ASGITransport(app=app)
	base_url = "http://test"
	async with AsyncClient(transport=transport, base_url=base_url) as client:
		response = await client.post("/api/v1/wallets/123e4567-e89b-43d3-a456-426614174003/operation", json={
			"operation_type": "WITHDRAW",
			"amount": 400,
		})
		assert response.status_code == 404


@pytest.mark.asyncio(loop_scope='session')
async def test_deposit_not_found():
	transport = ASGITransport(app=app)
	base_url = "http://test"
	async with AsyncClient(transport=transport, base_url=base_url) as client:
		response = await client.post("/api/v1/wallets/123e4567-e89b-43d3-a456-426614174003/operation", json={
			"operation_type": "DEPOSIT",
			"amount": 400,
		})
		assert response.status_code == 404


@pytest.mark.asyncio(loop_scope='session')
async def test_withdraw_more_money_than_have(test_wallet):
	transport = ASGITransport(app=app)
	base_url = "http://test"
	async with AsyncClient(transport=transport, base_url=base_url) as client:
		response = await client.post(f"/api/v1/wallets/{test_wallet.wallet_uuid}/operation", json={
			"operation_type": "WITHDRAW",
			"amount": 650,
		})
		assert response.status_code == 400
		assert "detail" in response.json()

		response_get = await client.get(f"/api/v1/wallets/{test_wallet.wallet_uuid}")
		assert response_get.status_code == 200
		assert response_get.json()['wallet_uuid'] == str(test_wallet.wallet_uuid)
		assert response_get.json()['balance'] == test_wallet.balance


@pytest.mark.asyncio(loop_scope='session')
async def test_operation_zero_amount(test_wallet):
	transport = ASGITransport(app=app)
	base_url = "http://test"
	async with AsyncClient(transport=transport, base_url=base_url) as client:
		response = await client.post(f"/api/v1/wallets/{test_wallet.wallet_uuid}/operation", json={
			"operation_type": "DEPOSIT",
			"amount": 0,
		})
		assert response.status_code == 422
		assert "detail" in response.json()


@pytest.mark.asyncio(loop_scope='session')
async def test_operation_negative_amount(test_wallet):
	transport = ASGITransport(app=app)
	base_url = "http://test"
	async with AsyncClient(transport=transport, base_url=base_url) as client:
		response = await client.post(f"/api/v1/wallets/{test_wallet.wallet_uuid}/operation", json={
			"operation_type": "DEPOSIT",
			"amount": -100,
		})
		assert response.status_code == 422
		assert "detail" in response.json()

		response_get = await client.get(f"/api/v1/wallets/{test_wallet.wallet_uuid}")
		assert response_get.status_code == 200
		assert response_get.json()['wallet_uuid'] == str(test_wallet.wallet_uuid)
		assert response_get.json()['balance'] == test_wallet.balance


@pytest.mark.asyncio(loop_scope='session')
async def test_invalid_operation_type(test_wallet):
	transport = ASGITransport(app=app)
	base_url = "http://test"
	async with AsyncClient(transport=transport, base_url=base_url) as client:
		response = await client.post(f"/api/v1/wallets/{test_wallet.wallet_uuid}/operation", json={
			"operation_type": "РАЗДЕЛИТЬ",
			"amount": 400,
		})
		assert response.status_code == 422
		assert "detail" in response.json()

		response_get = await client.get(f"/api/v1/wallets/{test_wallet.wallet_uuid}")
		assert response_get.status_code == 200
		assert response_get.json()['wallet_uuid'] == str(test_wallet.wallet_uuid)
		assert response_get.json()['balance'] == test_wallet.balance


@pytest.mark.asyncio(loop_scope='session')
async def test_invalid_uuid():
	transport = ASGITransport(app=app)
	base_url = "http://test"
	async with AsyncClient(transport=transport, base_url=base_url) as client:
		response = await client.post("/api/v1/wallets/Булочка/operation", json={
			"operation_type": "DEPOSIT",
			"amount": 400,
		})
		assert response.status_code == 422
		assert "detail" in response.json()


@pytest.mark.asyncio(loop_scope='session')
async def test_invalid_amount_type(test_wallet):
	transport = ASGITransport(app=app)
	base_url = "http://test"
	async with AsyncClient(transport=transport, base_url=base_url) as client:
		response = await client.post(
			f"/api/v1/wallets/{test_wallet.wallet_uuid}/operation",
			json={
				"operation_type": "DEPOSIT",
				"amount": 'Мильон',
			})
		assert response.status_code == 422
		assert "detail" in response.json()


@pytest.mark.asyncio(loop_scope='session')
async def test_concurrent_operations(test_wallet):
	transport = ASGITransport(app=app)
	base_url = "http://test"
	async with AsyncClient(transport=transport, base_url=base_url) as client:

		request1 = client.post(
			f"/api/v1/wallets/{test_wallet.wallet_uuid}/operation",
			json={
				"operation_type": "DEPOSIT",
				"amount": 500,
			})
		request2 = client.post(
			f"/api/v1/wallets/{test_wallet.wallet_uuid}/operation",
			json={
				"operation_type": "WITHDRAW",
				"amount": 450,
			})
		request3 = client.post(f"/api/v1/wallets/{test_wallet.wallet_uuid}/operation", json={
			"operation_type": "WITHDRAW",
			"amount": 100,
		})
		request4 = client.post(f'/api/v1/wallets/{test_wallet.wallet_uuid}/operation', json={
			"operation_type": "DEPOSIT",
			"amount": 400,
		})

		responses = await asyncio.gather(request1, request2, request3, request4)

		for response in responses:
			assert response.status_code == 200

		response_get = await client.get(f"/api/v1/wallets/{test_wallet.wallet_uuid}")
		assert response_get.status_code == 200
		assert response_get.json()['wallet_uuid'] == str(test_wallet.wallet_uuid)
		assert response_get.json()['balance'] == 950