"""Utility methods used by API"""

from typing import List

from flask import Request

from backend.models import RarityRef, RegionRef, RequestData


def digest_request(req: Request) -> RequestData:
    """Consume flask Request, return RequestData dictionary"""
    rarities: List[RarityRef] = []
    regions: List[RegionRef] = []
    no_limit = 0

    handle_key = {
        "common": lambda: rarities.append("Common"),
        "rare": lambda: rarities.append("Rare"),
        "epic": lambda: rarities.append("Epic"),
        "champion": lambda: rarities.append("Champion"),
        "bilgewater": lambda: regions.append("Bilgewater"),
        "demacia": lambda: regions.append("Demacia"),
        "freljord": lambda: regions.append("Freljord"),
        "ionia": lambda: regions.append("Ionia"),
        "noxus": lambda: regions.append("Noxus"),
        "piltover_and_zaun": lambda: regions.append("PiltoverZaun"),
        "shadow_isles": lambda: regions.append("ShadowIsles"),
        "targon": lambda: regions.append("Targon"),
    }

    known_keys = handle_key.keys()
    can_be_handled = lambda k, v: k in known_keys and v == "true"

    for key, value in req.args.to_dict().items():
        if can_be_handled(key, value):
            handle_key[key]()

    request_data: RequestData = {
        "region_refs": regions,
        "rarity_refs": rarities,
        "count": req.args.get(key="count", default=no_limit, type=int),
        "language": "en_us",
    }

    return request_data
