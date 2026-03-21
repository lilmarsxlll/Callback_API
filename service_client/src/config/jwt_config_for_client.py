import jwt

from src.config.logger_config import get_logger
from src.config.settings_for_client import settings

logger = get_logger(__name__)

JWT_SECRET_KEY = settings.JWT_SECRET_KEY
JWT_ALGORITHM = settings.JWT_ALGORITHM


def verify_jwt_token(token: str) -> bool:
    try:
        jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return True
    except jwt.ExpiredSignatureError:
        logger.error("JWT token expired")
        return False
    except jwt.InvalidTokenError:
        logger.error("JWT token invalid")
        return False
