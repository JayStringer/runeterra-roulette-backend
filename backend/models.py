from dataclasses import dataclass
from typing import Optional


@dataclass
class Regions:
    bligewater: Optional[bool]
    demacia: Optional[bool]
    freljord: Optional[bool]
    ionia: Optional[bool]
    noxus: Optional[bool]
    piltover_and_zaun: Optional[bool]
    shadow_isles: Optional[bool]
    targon: Optional[bool]


@dataclass
class Rarities:
    common: Optional[bool]
    rare: Optional[bool]
    epic: Optional[bool]
    champion: Optional[bool]


@dataclass
class Filter:
    count: int
    regions: Optional[Regions]
    rarities: Optional[Rarities]
