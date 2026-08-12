import asyncio
import httpx


async def main():
	async with httpx.AsyncClient() as client:
		url = (
			"http://127.0.0.1:8000/"
			"api/v1/wallets/123e4567-e89b-43d3-a456-426614174000/operation"
		)

		request_1 = client.post(url, json={
			"operation_type": "DEPOSIT",
			"amount": 500,
		})
		request_2 = client.post(url, json={
			"operation_type": "WITHDRAW",
			"amount": 200,
		})
		responses = await asyncio.gather(request_1, request_2)
		for response in responses:
			print(response.status_code, response.json())


asyncio.run(main())
