async def get_home_config(mongo, db_name):
    config = await mongo[db_name].configs.find_one({"key": "homePage"})
    if config and "value" in config:
        return config["value"]
    return None

async def get_home_data(mongo, db_name, user_id):
    # Fetch the config
    config = await get_home_config(mongo, db_name)
    if not config:
        return None
    # Fetch the actual data (user-specific)
    data_doc = await mongo[db_name]['home_data'].find_one({"user_id": user_id})
    if not data_doc:
        return None
    data = data_doc.get("data", {})
    # Conform data to config: only include fields present in config
    conformed = {k: data.get(k) for k in config.keys()}
    return conformed 