from redis import Redis
import os

r = Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True  # تا خروجی str باشه نه byte
)


MAX_ATTEMPTS = 5
LOCK_TIME = 300  # ۵ دقیقه

def check_login_attempts(username: str) -> bool:
    attempts = r.get(f"login_attempts:{username}")
    if attempts and int(attempts) >= MAX_ATTEMPTS:
        return False  # کاربر قفل شده
    return True

def register_failed_attempt(username: str):
    key = f"login_attempts:{username}"
    attempts = r.get(key)
    if attempts:
        r.incr(key)
    else:
        r.set(key, 1, ex=LOCK_TIME)

def reset_attempts(username: str):
    r.delete(f"login_attempts:{username}")
