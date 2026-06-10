from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")



API_KEY_DATA = {
    API_KEY: {
        "credits": 5,
        "reset_time": datetime.now(timezone.utc) + timedelta(hours=24) #lock time of first request
    }
}
