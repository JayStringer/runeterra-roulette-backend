"""API for Runterra Roulette Web Application"""

from flask import Flask, Request, jsonify, request
from flask_cors import CORS

from models import Filter, Rarities, Regions

app = Flask(__name__)
CORS(app)


def _digest_url_args(request: Request) -> Filter:
    rarities = Rarities(
        common=request.args.get('common'),
        rare=request.args.get('rare'),
        epic=request.args.get('epic'),
        champion=request.args.get('champion'),
        
    )
    print(rarities)

    return None


@app.route("/cards", methods=["GET"])
def get_cards():
    _digest_url_args(request)
    return jsonify({"message": "Nice request m8"})


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
