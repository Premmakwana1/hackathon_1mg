import json
import os

CONFIG_PATH = os.getenv("CONFIG_PATH", os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config.json"))

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

mongo_conf = config["MONGO"]

DB_NAME = os.getenv("MONGO_DB_NAME", mongo_conf["DB_NAME"])
MONGO_HOSTS = os.getenv("MONGO_HOSTS", ",".join(mongo_conf["HOSTS"]))
MONGO_USER = os.getenv("MONGO_USER", mongo_conf.get("USER", ""))
MONGO_PASS = os.getenv("MONGO_PASS", mongo_conf.get("PASS", ""))

if isinstance(MONGO_HOSTS, str):
    MONGO_HOSTS = MONGO_HOSTS.split(",")

MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOSTS[0]}/{DB_NAME}?retryWrites=true&w=majority&ssl=true&tlsAllowInvalidCertificates=true"

API_VERSION = config.get("API_VERSION", "v1") 