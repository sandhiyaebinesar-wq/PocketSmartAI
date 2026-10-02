import hashlib
import hmac
import os
from datetime import datetime, timedelta, timezone

import jwt

from Backend.settings import get_settings


ALGORITHM = "HS256"


def hash_password(password):
    salt = os.urandom(16)

    password_hash = hashlib.scrypt(
        password.encode(),
        salt=salt,
        n=2**14,
        r=8,
        p=1
    )

    return (
        "scrypt$"
        + salt.hex()
        + "$"
        + password_hash.hex()
    )


def verify_password(password, stored_password):
    try:
        scheme, salt, stored_hash = stored_password.split("$")

        if scheme != "scrypt":
            return False

        password_hash = hashlib.scrypt(
            password.encode(),
            salt=bytes.fromhex(salt),
            n=2**14,
            r=8,
            p=1
        )

        return hmac.compare_digest(
            password_hash.hex(),
            stored_hash
        )

    except Exception:
        return False


def create_token(user_id):
    settings = get_settings()

    now = datetime.now(timezone.utc)

    expiry = (
        now
        + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    )

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": expiry
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=ALGORITHM
    )


def decode_token(token):
    settings = get_settings()

    payload = jwt.decode(
        token,
        settings.secret_key,
        algorithms=[ALGORITHM]
    )

    return int(payload["sub"])