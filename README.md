# pwiki

An OSRS price wiki client

## Purpose

Provide an API for the OSRS price wiki at
https://oldschool.runescape.wiki/w/RuneScape:Real-time_Prices that behaves
nicely by default -- requiring a descriptive User-Agent, not abusing their
servers, and strongly typing the responses.

## Installation

```bash
python -m pip install -e git+https://github.com/hmusgrave/pwiki.git#egg=pwiki
```

## Examples
```python
import asyncio
from pwiki.client import Client

async def main():
    async with Client('price exploration -- explorer1@gmail.com') as client:
        mapping = await client.mapping()
        whip = next(x for x in mapping if x.name == 'Abyssal whip')
        last_whip_trades = await client.latest(item = whip.item)
        print(last_whip_trades)

asyncio.run(main())
```

## Status
Contributions welcome. I'll check back on this repo at least once per month.
