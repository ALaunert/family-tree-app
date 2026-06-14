from pydantic import BaseModel, ConfigDict, Field

from app.models.relationship import RelationshipType
from app.models.user import UserRole
from app.schemas.person import PersonRead


class TreeRelationshipRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    relationship_type: RelationshipType = Field(alias="type")
    source_person_id: int = Field(alias="sourcePersonId")
    target_person_id: int = Field(alias="targetPersonId")


class TreeRead(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    viewer_role: UserRole = Field(alias="viewerRole")
    people: list[PersonRead]
    relationships: list[TreeRelationshipRead]
