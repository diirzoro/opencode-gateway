from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50, pattern=r"^[A-Za-z0-9_.-]+$")
    email: EmailStr
    password: str = Field(min_length=10, max_length=128)
    phone: str = Field(min_length=6, max_length=30)
    postal_code: str = Field(min_length=2, max_length=24)
    country_id: int
    region_id: int | None = None
    city_id: int | None = None
    @field_validator("password")
    @classmethod
    def strong_password(cls, value):
        if not any(c.isalpha() for c in value) or not any(c.isdigit() for c in value):
            raise ValueError("Password must contain a letter and a number")
        return value

class LoginRequest(BaseModel):
    identity: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=1, max_length=128)

class ProfilePatch(BaseModel):
    phone: str | None = Field(None, min_length=6, max_length=30)
    postal_code: str | None = Field(None, min_length=2, max_length=24)
    country_id: int | None = None
    region_id: int | None = None
    city_id: int | None = None
    preferred_language: str | None = Field(None, pattern="^(ar|en)$")
    preferred_theme: str | None = Field(None, pattern="^(light|dark)$")

class LocationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    code: str | None = None

class UserOut(BaseModel):
    id: str
    username: str
    email: str
    phone: str
    postal_code: str
    country: str
    region: str | None
    city: str | None
    role: str
    status: str
    preferred_language: str
    preferred_theme: str
    trial_started_at: datetime
    trial_ends_at: datetime
    trial_remaining_days: int
    last_login_at: datetime | None
