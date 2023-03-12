import aiohttp  

class Api:
    async def request(self, action, params=None):
        async with aiohttp.ClientSession() as session:
            try:
                url = f"{self.base_url}{action}"
                response = await session.post(url, params=params)
                return await response.json()
            except Exception as e:
                print(f"Error sending request: {e}")

    async def sendMessage(self, params):
        await self.request("sendMessage", params)

    async def sendDice(self, params=None):
        await self.request("sendDice", params)