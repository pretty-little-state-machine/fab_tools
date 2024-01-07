"""
Helpers for parsing Fabrary GraphQL

There's no Fabrary API so the easiest way to extract deck information is to just watch the GraphQL queries for loading a
deck and then dumping that JSON into a file to be parsed.
"""
from typing import Dict
import json


def load_graphql_result(json_filename: str) -> Dict:
    with open(json_filename, encoding="utf-8", errors="ignore") as json_data:
        return json.load(json_data, strict=False)
