"""API for Runterra Roulette Web Application"""

from pprint import pprint

from flask import Flask, Request, jsonify, request
from flask_cors import CORS
from requests import Response

from models import Filter, Rarities, Regions

app = Flask(__name__)
CORS(app)


# def _digest_url_args(req: Request) -> Filter:
#     rarities = Rarities(
#         common=request.args.get("common"),
#         rare=request.args.get("rare"),
#         epic=request.args.get("epic"),
#         champion=request.args.get("champion"),
#     )
#     print(rarities)

#     return None


def digest_request(req: Request):
    rarities = []
    regions = []
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

    # Assignment to keep pylint happy
    _ = [handle_key[key]() for key, value in request.args.to_dict().items() if value == "true"]

    return {
        "regionRefs": regions,
        "rarityRefs": rarities,
        "limit": req.args.get("count", no_limit),
    }


@app.route("/cards", methods=["GET"])
def get_cards():
    """"""
    pprint(digest_request(req=request))
    return jsonify({"message": "Nice request m8"})


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
