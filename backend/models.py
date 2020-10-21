"""Models to assist with type hinting"""

from dataclasses import dataclass
from typing import List, Literal, Optional, TypedDict

RegionRef = Literal[
  "BilgeWater",
  "Demacia",
  "Freljord",
  "Ionia",
  "Noxus",
  "PiltoverZaun",
  "ShadowIsles",
  "Targon"
]

RarityRef = Literal[
  "Common",
  "Rare",
  "Epic",
  "Champion"
]

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


class CardAssets(TypedDict):
    gameAbsolutePath: str
    fullAbsolutePath: str


class Card(TypedDict):
    associatedCards: List[str]
    associatedCardRefs: List[str]
    assets: List[CardAssets]
    region: str
    regionRef: str
    attack: int
    cost: int
    health: int
    description: str
    descriptionRaw: str
    levelupDescription: str
    levelupDescriptionRaw: str
    flavorText: str
    artistName: str
    name: str
    cardCode: str
    keywords: List[str]
    keywordRefs: List[str]
    spellSpeed: str
    spellSpeedRef: str
    rarity: str
    rarityRef: str
    subtype: str
    subtypes: List[str]
    supertype: str
    type: str
    collectible: bool
    set: str


class CardDoc(Card):
    _id: str
