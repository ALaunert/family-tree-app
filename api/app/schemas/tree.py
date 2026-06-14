from pydantic import BaseModel, ConfigDict, Field

from app.models.user import UserRole
from app.schemas.person import PersonRead
from app.schemas.relationship import RelationshipRead


class TreeRead(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    viewer_role: UserRole = Field(alias="viewerRole")
    people: list[PersonRead]
    relationships: list[RelationshipRead]
