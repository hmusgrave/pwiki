import httpx, aiolimit
from enum import Enum

class PriceBaseUrl(Enum):
    Default = 'https://prices.runescape.wiki/api/v1/osrs'
    Deadman = 'https://prices.runescape.wiki/api/v1/dmm'

class Session(httpx.AsyncClient):
    def __init__(self, user_agent: str, *args, endpoint: PriceBaseUrl = PriceBaseUrl.Default, allow_short_agent: bool = False, **kwargs):
        guide = 'https://oldschool.runescape.wiki/w/RuneScape:Real-time_Prices#Acceptable_use_policy'
        if (not user_agent or len(user_agent) < 10) and not allow_short_agent:
            raise Exception(f'Please set a descriptive user agent.\nSee {guide} for details.\nPass allow_short_agent=True to bypass this check.')
        headers = {'user-agent': user_agent}
        super().__init__(*args, headers=headers, base_url=endpoint.value, **kwargs)
        self.limiters = [
            aiolimit.Limiter(1, 5),  # at most 5 requests in 1 second
            aiolimit.Limiter(60, 60),  # at most 60 requests in 1 minute
        ]

    async def _send(self, request):
        async def _f(limiters):
            if not limiters:
                return await self.send(request)
            return await self.limiters[0].run(_f(limiters[1:]))
        return await _f(self.limiters)
