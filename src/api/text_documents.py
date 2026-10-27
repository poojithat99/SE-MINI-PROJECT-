
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from src.api.dependencies import get_current_user
from src.repositories.user_repository import SessionLocal, User
from src.repositories.admin_repository import record_audit_event
from src.services.document_service import (
    upload_document,
    process_document,
    list_user_documents,
    get_user_document,
    get_download_info,
    delete_user_document,
    edit_text_document,
)

router = APIRouter(prefix="/api/text-documents", tags=["Text Documents"])


class TextDocumentInput(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=100000)
    category: str | None = None


def resolve_owner(account: dict):
    username = str(account.get("username") or "").strip()
    user_id = account.get("sub") or account.get("user_id") or account.get("id")

    with SessionLocal() as db:
        owner = None

        if username:
            owner = (
                db.query(User)
                .filter(User.username == username)
                .first()
            )

        if owner is None and user_id is not None:
            try:
                owner = db.get(User, int(user_id))
            except (TypeError, ValueError):
                owner = None

        if owner is None:
            raise HTTPException(status_code=401, detail="User account not found")

        # Return plain values so they remain usable after the session closes.
        return {"id": owner.id, "username": owner.username}


def public_text_document(item: dict, owner_id: int) -> dict:
    content = item.get("extracted_text") or ""

    if not content:
        try:
            path, filename = get_download_info(owner_id, item["id"])
            if filename.lower().endswith(".txt"):
                content = path.read_text(encoding="utf-8-sig")
        except (FileNotFoundError, OSError):
            content = ""

    return {
        "id": item["id"],
        "title": item.get("title", ""),
        "content": content,
        "category": item.get("category") or "Uncategorized",
    }


@router.get("")
def list_text_documents(
    search: str = "",
    account: dict = Depends(get_current_user),
):
    owner = resolve_owner(account)
    result = list_user_documents(owner["id"])

    documents = [
        public_text_document(item, owner["id"])
        for item in result["items"]
    ]

    search_term = search.strip().casefold()
    if search_term:
        documents = [
            document for document in documents
            if search_term in document["title"].casefold()
        ]

    return documents


@router.post("", status_code=status.HTTP_201_CREATED)
def create_text_document(
    data: TextDocumentInput,
    account: dict = Depends(get_current_user),
):
    title = data.title.strip()
    content = data.content.strip()

    if not title or not content:
        raise HTTPException(status_code=400, detail="Title and content are required")

    owner = resolve_owner(account)
    filename = f"{title[:180]}.txt"

    try:
        result = upload_document(
            owner_id=owner["id"],
            filename=filename,
            content=content.encode("utf-8"),
            title=title,
        )
        process_document(result["id"], owner["id"])
        saved = get_user_document(owner["id"], result["id"])
    except (ValueError, FileNotFoundError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    record_audit_event(
        user_id=owner["id"],
        username=owner["username"],
        action="text_document_create",
        details=f"Text document created: {title}",
    )

    return {
        "id": saved["id"],
        "title": saved["title"],
        "content": saved.get("extracted_text", content),
    }


@router.put("/{document_id}")
def update_text_document(
    document_id: int,
    data: TextDocumentInput,
    account: dict = Depends(get_current_user),
):
    title = data.title.strip()
    content = data.content.strip()

    if not title or not content:
        raise HTTPException(status_code=400, detail="Title and content are required")

    owner = resolve_owner(account)

   
    try:
        get_user_document(owner["id"], document_id)
        saved = edit_text_document(
            owner["id"],
            document_id,
            title,
            content,
            category=data.category,
        )
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
        saved = edit_text_document(
            owner["id"],
            document_id,
            title,
            content,
            category=data.category,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Document not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    record_audit_event(
        user_id=owner["id"],
        username=owner["username"],
        action="text_document_update",
        details=f"Text document updated: {title}",
    )

    return {
        "id": saved["id"],
        "title": saved["title"],
        "content": saved.get("extracted_text", content),
    }


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_text_document(
    document_id: int,
    account: dict = Depends(get_current_user),
):
    owner = resolve_owner(account)

    try:
        get_user_document(owner["id"], document_id)
        delete_user_document(owner["id"], document_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Document not found") from exc

    record_audit_event(
        user_id=owner["id"],
        username=owner["username"],
        action="text_document_delete",
        details=f"Text document deleted: {document_id}",
    )

    return None
