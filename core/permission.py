def is_enabled(config: dict, section: str) -> bool:
    try:
        return config[section].get("enabled", False)
    except KeyError:
        return False

def is_allowed(config: dict, section: str, key: str) -> bool:
    try:
        return config[section].get(key, False)
    except KeyError:
        return False
