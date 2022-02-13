from pwiki.schema import *
from pwiki.session import *
import pwiki.request as request
from typing import List, Dict, Optional
from datetime import datetime, timezone

def _maybe(T, val, time):
    if val is None or time is None or time == 0:
        return None
    return T(val, time)

class Client(Session):
    def __init__(self, user_agent: str, *args, endpoint: PriceBaseUrl = PriceBaseUrl.Default, allow_short_agent: bool = False, **kwargs):
        super().__init__(user_agent, *args, endpoint=endpoint, allow_short_agent=allow_short_agent, **kwargs)

    async def latest(self, item: Optional[Id] = None) -> Dict[Id, Trade]:
        resp = await self._send(request.latest(self, item))
        resp.raise_for_status()
        return {
            Id(int(k)): Latest(_maybe(Trade, v['high'], v['highTime']), _maybe(Trade, v['low'], v['lowTime']))
            for k,v in resp.json()['data'].items()
        }

    async def mapping(self) -> List[Summary]:
        resp = await self._send(request.mapping(self))
        resp.raise_for_status()
        return [
            Summary(
                examine = x['examine'],
                item = Id(x['id']),
                lowalch = Price(x.get('lowalch')),
                highalch = Price(x.get('highalch')),
                value = Price(x['value']),
                trade_limit = Count(x.get('limit')),
                is_members = x['members'],
                icon = Path(x['icon']),
                name = x['name'],
            )
            for x in resp.json()
        ]

    async def prices(self, interval: StepWidth, ts: Optional[datetime] = None, ignore_extra_seconds: bool = False) -> Steps:
        resp = await self._send(request.prices(self, interval, ts, ignore_extra_seconds))
        resp.raise_for_status()
        resp = resp.json()
        return Steps(
            {
                Id(int(k)): Step(
                    _maybe(Stats, v['avgHighPrice'], v['highPriceVolume']),
                    _maybe(Stats, v['avgLowPrice'], v['lowPriceVolume']),
                )
                for k,v in resp['data'].items()
            },
            datetime.fromtimestamp(resp['timestamp'], timezone.utc),
        )

    async def timeseries(self, item: Id, interval: StepWidth) -> List[TimedStep]:
        resp = await self._send(request.timeseries(self, item, interval))
        resp.raise_for_status()
        return [
            TimedStep(
                _maybe(Stats, d['avgHighPrice'], d['highPriceVolume']),
                _maybe(Stats, d['avgLowPrice'], d['lowPriceVolume']),
                datetime.fromtimestamp(d['timestamp'], timezone.utc),
            )
            for d in resp.json()['data']
        ]

    async def icon(self, item: Path) -> bytes:
        resp = await self._send(request.icon(self, item))
        resp.raise_for_status()
        return resp.content
