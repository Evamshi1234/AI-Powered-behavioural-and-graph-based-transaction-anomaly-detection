from datetime import datetime

from pydantic import BaseModel, Field


class ProfileCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    age: int = Field(ge=1, le=120)
    gender: str = "prefer_not_to_say"
    conditions: str = ""
    medications: str = ""
    allergies: str = ""
    health_goals: str = ""


class ProfileUpdate(ProfileCreate):
    pass


class ProfileResponse(ProfileCreate):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ConversationCreate(BaseModel):
    profile_id: int
    title: str = "New conversation"


class ConversationResponse(BaseModel):
    id: int
    profile_id: int
    title: str
    created_at: datetime

    model_config = {"from_attributes": True}


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatRequest(BaseModel):
    profile_id: int
    conversation_id: int | None = None
    message: str = Field(min_length=1, max_length=4000)


class ChatResponse(BaseModel):
    conversation_id: int
    reply: str
    safety_flags: list[str] = []
    rag_sources: list[str] = []
    provider: str
