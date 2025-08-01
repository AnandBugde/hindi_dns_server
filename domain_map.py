# domain_map.py

import json
from config import DOMAIN_MAP_FILE

def load_domain_map():
    with open(DOMAIN_MAP_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
