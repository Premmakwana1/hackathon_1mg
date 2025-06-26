import json
import os

CONFIG_PATH = os.getenv("CONFIG_PATH", os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config.json"))

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

mongo_conf = config["MONGO"]

DB_NAME = mongo_conf["DB_NAME"]
MONGO_HOSTS = mongo_conf["HOSTS"]
MONGO_USER = mongo_conf.get("USER", "")
MONGO_PASS = mongo_conf.get("PASS", "")

MONGO_URI = f"mongodb://{','.join(MONGO_HOSTS)}/{DB_NAME}" 