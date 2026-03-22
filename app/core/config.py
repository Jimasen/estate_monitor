# app/core/config.py

import logging
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # ----------------------------------------
    # APP
    # ----------------------------------------
    APP_ENV: str = "development"
    APP_NAME: str
    APP_HOST: str

    # ----------------------------------------
    # DATABASE
    # ----------------------------------------
    DATABASE_URL_MYSQL: str
    DATABASE_URL_POSTGRES: str | None = None

    # ----------------------------------------
    # EMAIL
    # ----------------------------------------
    EMAIL_USER: str | None = None
    EMAIL_PASSWORD: str | None = None
    EMAIL_ENABLED: bool = False

    # ----------------------------------------
    # SMS
    # ----------------------------------------
    SMS_API_KEY: str | None = None
    SMS_SENDER: str | None = None
    SMS_ENABLED: bool = False

    # ----------------------------------------
    # SECURITY
    # ----------------------------------------
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    SESSION_SECRET_KEY: str

    # ----------------------------------------
    # WHATSAPP
    # ----------------------------------------
    WHATSAPP_PHONE_ID: str | None = None
    WHATSAPP_ACCESS_TOKEN: str | None = None
    WHATSAPP_VERIFY_TOKEN: str | None = None
    WHATSAPP_ENABLED: bool = False

    # ----------------------------------------
    # OWNER NOTIFICATION
    # ----------------------------------------
    OWNER_PHONE_NUMBER: str | None = None

    # ----------------------------------------
    # PAYSTACK
    # ----------------------------------------
    PAYSTACK_SECRET_KEY: str | None = None
    PAYSTACK_WEBHOOK_SECRET: str | None = None

    # ----------------------------------------
    # FLUTTERWAVE
    # ----------------------------------------
    FLUTTERWAVE_SECRET_HASH: str | None = None

    # ----------------------------------------
    # DATABASE SWITCH (FIXED í´¥)
    # ----------------------------------------
    @property
    def DATABASE_URL(self) -> str:
        if self.DATABASE_URL_POSTGRES:
            logging.info("âœ… Using PostgreSQL database")
            return self.DATABASE_URL_POSTGRES

        logging.info("âœ… Using MySQL database")
        return self.DATABASE_URL_MYSQL

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
