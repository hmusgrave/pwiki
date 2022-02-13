from pwiki.schema import *
from typing import Optional
from datetime import datetime, timezone
import httpx
from warnings import warn

def latest(client: httpx.Client, item: Optional[Id] = None) -> httpx.Request:
    params = {}
    if item is not None:
        params['id'] = int(item)
    return client.build_request(
        'GET',
        '/latest',
        params = params
    )

def mapping(client: httpx.Client) -> httpx.Request:
    return client.build_request('GET', '/mapping')

def _normalize_ts(ts: datetime, ignore: bool, width_sec: int) -> datetime:
    result = int(ts.timestamp() // width_sec * width_sec)
    if ignore:
        return result
    if result != ts.timestamp():
        warn(f'Timestamps must be normalized to {width_sec} second boundaries. Pass ignore_extra_seconds=True to suppress this warning.')
    return result;

def prices(client: httpx.Client, interval: StepWidth, ts: Optional[datetime] = None, ignore_extra_seconds: bool = False) -> httpx.Request:
    params = {}
    end = '5m'
    if ts is not None:
        i = None
        if interval == StepWidth.m5:
            i = 5
        elif interval == StepWidth.h1:
            i = 60
            end = '1h'
        elif interval == StepWidth.h6:
            raise ValueError('Wiki does not support 6h intervals for this endpoint')
        else:
            raise NotImplementedError()
        params['timestamp'] = _normalize_ts(ts, ignore_extra_seconds, i * 60)

    return client.build_request(
        'GET',
        f'/{end}',
        params = params
    )

def timeseries(client: httpx.Client, item: Id, step: StepWidth) -> httpx.Request:
    params = {'id': int(item), 'timestep': step.value}
    return client.build_request(
        'GET',
        '/timeseries',
        params = params
    )

def _normalize_frag(path: str) -> str:
    return path.replace(' ', '_')

def icon(client: httpx.Client, item: Path) -> httpx.Request:
    return client.build_request(
        'GET',
        f'https://oldschool.runescape.wiki/images/{_normalize_frag(item)}'
    )
