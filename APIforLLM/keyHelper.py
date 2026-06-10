from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Header
from keyInfo import API_KEY_DATA


def get_user_data(api_key: str):
    data = API_KEY_DATA.get(api_key)

    if not data:
        return None

    # reset when required
    if datetime.now(timezone.utc) >= data["reset_time"]:
        data["credits"] = 5
        data["reset_time"] = datetime.now(timezone.utc) + timedelta(hours=24)

    return data


def verify_api_key(x_api_key: str = Header(None)):

    user = get_user_data(x_api_key)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    if user["credits"] <= 0:
        raise HTTPException(status_code=429, detail="No credits left for today")

    return x_api_key
