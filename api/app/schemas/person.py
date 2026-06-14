from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator


FULL_NAME_MAX_LENGTH = 200


class PersonCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    full_name: str = Field(alias="fullName", max_length=FULL_NAME_MAX_LENGTH)
    birth_date: date | None = Field(default=None, alias="birthDate")
    death_date: date | None = Field(default=None, alias="deathDate")
    notes: str | None = None

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("fullName cannot be blank")
        return stripped


class PersonUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    full_name: str | None = Field(
        default=None,
        alias="fullName",
        max_length=FULL_NAME_MAX_LENGTH,
    )
    birth_date: date | None = Field(default=None, alias="birthDate")
    death_date: date | None = Field(default=None, alias="deathDate")
    notes: str | None = None

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str | None) -> str | None:
        if value is None:
            raise ValueError("fullName cannot be null")

        stripped = value.strip()
        if not stripped:
            raise ValueError("fullName cannot be blank")
        return stripped


class PersonRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    full_name: str = Field(alias="fullName")
    birth_date: date | None = Field(default=None, alias="birthDate")
    death_date: date | None = Field(default=None, alias="deathDate")
    notes: str | None = None
