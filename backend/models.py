"""Models to assist with type hinting"""

from typing import List, Literal, TypedDict

RegionRef = Literal[
    "Bilgewater", "Demacia", "Freljord", "Ionia", "Noxus", "PiltoverZaun", "ShadowIsles", "Targon"
]

RarityRef = Literal["Common", "Rare", "Epic", "Champion"]


class RequestData(TypedDict):
    region_refs: List[RegionRef]
    rarity_refs: List[RarityRef]
    count: int
    language: str


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
