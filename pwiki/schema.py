from dataclasses import dataclass
from typing import Dict, Optional, NewType, List
from datetime import datetime
from enum import Enum

Id = NewType('Id', int)
Price = NewType('Price', int)
Count = NewType('Count', int)
Path = NewType('Path', str)

# latest

@dataclass
class Trade:
    value: Price
    ts: datetime

@dataclass
class Latest:
    high: Optional[Trade]
    low: Optional[Trade]

# mapping

@dataclass
class Summary:
    examine: str
    item: Id
    lowalch: Price
    highalch: Price
    value: Price
    trade_limit: Count
    is_members: bool
    icon: Path
    name: str

# 5m, 1h

@dataclass
class Stats:
    mean: Price
    volume: Count

@dataclass
class Step:
    high: Optional[Stats]
    low: Optional[Stats]

@dataclass
class Steps:
    data: Dict[Id, Step]
    timestamp: datetime

# timeseries

@dataclass
class TimedStep:
    high: Optional[Stats]
    low: Optional[Stats]
    timestamp: datetime

class StepWidth(Enum):
    m5 = '5m'
    h1 = '1h'
    h6 = '6h'
