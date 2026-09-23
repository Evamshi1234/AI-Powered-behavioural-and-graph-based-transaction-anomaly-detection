from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Conversation, Message, PatientProfile
from app.schemas import ChatRequest, ChatResponse, ConversationResponse, MessageResponse
from app.services.llm import build_profile_context, generate_reply
from app.services.rag import retrieve_context
from app.services.safety import detect_emergency, emergency_response

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.get("/conversations/{profile_id}", response_model=list[ConversationResponse])
def list_conversations(profile_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Conversation)
        .filter(Conversation.profile_id == profile_id)
        .order_by(Conversation.created_at.desc())
        .all()
    )


@router.get("/messages/{conversation_id}", response_model=list[MessageResponse])
def list_messages(conversation_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .all()
    )


@router.post("", response_model=ChatResponse)
async def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    profile = db.get(PatientProfile, payload.profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    safety_flags = detect_emergency(payload.message)

    if payload.conversation_id:
        conversation = db.get(Conversation, payload.conversation_id)
        if not conversation or conversation.profile_id != profile.id:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = Conversation(profile_id=profile.id, title=payload.message[:60])
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    history = [
        {"role": m.role, "content": m.content}
        for m in (
            db.query(Message)
            .filter(Message.conversation_id == conversation.id)
            .order_by(Message.created_at.asc())
            .all()
        )
    ]

    user_msg = Message(conversation_id=conversation.id, role="user", content=payload.message)
    db.add(user_msg)

    if "possible_emergency" in safety_flags:
        reply_text = emergency_response()
        provider = "safety"
        rag_sources: list[str] = []
    else:
        profile_ctx = build_profile_context(profile)
        rag_context, rag_sources = retrieve_context(payload.message, profile_ctx)
        reply_text, provider = await generate_reply(payload.message, profile, history, rag_context)

    assistant_msg = Message(conversation_id=conversation.id, role="assistant", content=reply_text)
    db.add(assistant_msg)
    db.commit()

    return ChatResponse(
        conversation_id=conversation.id,
        reply=reply_text,
        safety_flags=safety_flags,
        rag_sources=rag_sources,
        provider=provider,
    )
