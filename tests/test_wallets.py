import pytest
from main import app
from httpx import AsyncClient, ASGITransport

TRANSPORT = ASGITransport(app=app)


@pytest.mark.asyncio(loop_scope='session')
async def test_get_wallet(test_wallet):
	transport = TRANSPORT
	base_url = "http://test"
	async with AsyncClient(transport=transport, base_url=base_url) as client:
		response = await client.get(f"/api/v1/wallets/{test_wallet.wallet_uuid}")
		assert response.status_code == 200
		assert response.json()['wallet_uuid'] == str(test_wallet.wallet_uuid)
		assert response.json()['balance'] == test_wallet.balance
