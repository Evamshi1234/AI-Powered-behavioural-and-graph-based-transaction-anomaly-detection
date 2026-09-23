import json
from pathlib import Path

KB_PATH = Path(__file__).resolve().parent.parent / "data" / "knowledge_base.json"


def _load_kb() -> list[dict]:
    with KB_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def _tokenize(text: str) -> set[str]:
    return {t.strip().lower() for t in text.replace(",", " ").split() if len(t.strip()) > 2}


def retrieve_context(query: str, profile_context: str, top_k: int = 3) -> tuple[str, list[str]]:
    kb = _load_kb()
    query_tokens = _tokenize(query + " " + profile_context)

    scored: list[tuple[float, dict]] = []
    for doc in kb:
        doc_tokens = set(doc.get("topics", [])) | _tokenize(doc.get("content", "") + " " + doc.get("title", ""))
        overlap = len(query_tokens & doc_tokens)
        if overlap:
            scored.append((overlap, doc))

    scored.sort(key=lambda x: x[0], reverse=True)
    selected = [doc for _, doc in scored[:top_k]]

    if not selected and profile_context:
        profile_lower = profile_context.lower()
        for doc in kb:
            if any(topic in profile_lower for topic in doc.get("topics", [])):
                selected.append(doc)
                if len(selected) >= top_k:
                    break

    if not selected:
        selected = kb[:2]

    context_blocks = [f"[{d['title']}]: {d['content']}" for d in selected]
    sources = [d["title"] for d in selected]
    return "\n\n".join(context_blocks), sources
