from pydantic import BaseModel, ConfigDict, Field

from app.models.relationship import RelationshipType


class RelationshipCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    relationship_type: RelationshipType = Field(alias="relationshipType")
    source_person_id: int = Field(alias="sourcePersonId")
    target_person_id: int = Field(alias="targetPersonId")


class RelationshipRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    relationship_type: RelationshipType = Field(alias="relationshipType")
    source_person_id: int = Field(alias="sourcePersonId")
    target_person_id: int = Field(alias="targetPersonId")
