import json

import requests


def get_legal_name(lei):
    """
    Retrieve the legal name
    """
    url = f"https://leilookup.gleif.org/api/v2/leirecords?lei={lei}"
    try:
        res = requests.get(url).text
        return json.loads(res)[0]["Entity"]["LegalName"]["$"]
    except KeyError:
        raise ValueError("LEI not found")
