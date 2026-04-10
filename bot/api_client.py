import aiohttp


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self._session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def get_game_card(self, mode: str) -> dict:
        session = await self._get_session()
        async with session.get(
            f"{self.base_url}/api/v1/game-card", params={"mode": mode}
        ) as resp:
            data = await resp.json()
            return data["data"]

    async def get_rules(self) -> str:
        session = await self._get_session()
        async with session.get(f"{self.base_url}/api/v1/rules") as resp:
            data = await resp.json()
            return data["data"]["rules"]

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()
