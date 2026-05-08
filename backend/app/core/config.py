"""
Configuration Settings for C.O.V.E.R.T Backend
"""

from typing import List
from pydantic_settings import BaseSettings
from pydantic import validator


class Settings(BaseSettings):
    """Application settings"""

    # ===== Application =====
    APP_NAME: str = "C.O.V.E.R.T"
    ENVIRONMENT: str = "production"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # ===== Security =====
    SECRET_KEY: str = "c0v3rt-s3cr3t-pr0duct10n-k3y-49-b4s3-s3p0l14"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # ===== CORS =====
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000", "https://covert-chi.vercel.app"]

    # ===== Database =====
    DATABASE_URL: str = "postgresql+asyncpg://covert_user:covert_password@localhost:5432/covert_db"
    DB_ECHO: bool = False

    # ===== Redis =====
    REDIS_URL: str = "redis://localhost:6379/0"

    # ===== IPFS =====
    IPFS_API_URL: str = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    IPFS_GATEWAY_URL: str = "https://gateway.pinata.cloud"
    PINATA_API_KEY: str = "9fcc6f3c8188c2e741b3"
    PINATA_SECRET_KEY: str = "03984567a6849a7e820618c612a7e77607023c936896cb572732834f5a66f968"
    WEB3_STORAGE_TOKEN: str = ""

    # ===== Blockchain =====
    RPC_URL: str = "https://sepolia.base.org"
    CHAIN_ID: int = 84532  # Base Sepolia
    COMMITMENT_REGISTRY_ADDRESS: str = "0x6da91E0248E1177A472C7Ec905493f4ddaF9c0F3"
    DAILY_ANCHOR_ADDRESS: str = "0x7E10Bc04DbC2A48e6a8F54Dc488Aa6da6755d223"
    COV_CREDITS_ADDRESS: str = "0x7b96Ea73892baE3a3c875b2701F2D1A3031F3159"
    COVERT_BADGES_ADDRESS: str = "0x171656f685c21EE56c5db5a264503B93B714a95a"
    COVERT_PROTOCOL_ADDRESS: str = "0x1C90D50Be7661Dc48106527F1657b8D8F12b5F60"
    AUTOMATION_PRIVATE_KEY: str = ""  # Private key for AUTOMATION_ROLE signer (reviewer role management)

    # ===== Rate Limiting =====
    RATE_LIMIT_SUBMISSIONS: int = 10  # per hour
    RATE_LIMIT_GENERAL: int = 100  # per hour

    # ===== File Upload =====
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100 MB
    ALLOWED_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png", ".pdf", ".mp4", ".zip"]

    # ===== Email (Gmail SMTP) =====
    GMAIL_ADDRESS: str = ""
    GMAIL_APP_PASSWORD: str = ""
    FRONTEND_URL: str = "http://localhost:5173"

    # ===== Routing =====
    FOLLOWUP_DAYS: int = 7  # days between followup emails to non-responsive departments

    # ===== Monitoring =====
    SENTRY_DSN: str = ""
    LOG_LEVEL: str = "INFO"

    @validator("SECRET_KEY")
    def check_secret_key(cls, v, values):
        env = values.get("ENVIRONMENT", "development")
        if env == "production" and v == "CHANGE_THIS_IN_PRODUCTION":
            raise ValueError("SECRET_KEY must be changed from default in production")
        return v

    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            origins = [origin.strip() for origin in v.split(",")]
        else:
            origins = list(v)
        # Always include the production frontend
        vercel_default = "https://frontend-xi-ecru-10.vercel.app"
        vercel_custom = "https://covert-protocol.vercel.app"
        vercel_new = "https://covert-49.vercel.app"
        if vercel_default not in origins:
            origins.append(vercel_default)
        if vercel_custom not in origins:
            origins.append(vercel_custom)
        if vercel_new not in origins:
            origins.append(vercel_new)
        return origins

    @validator("DATABASE_URL", pre=True)
    def parse_database_url(cls, v):
        if isinstance(v, str) and v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql+asyncpg://", 1)
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
