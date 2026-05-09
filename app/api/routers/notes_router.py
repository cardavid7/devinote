from fastapi import APIRouter, status
from typing import List
from app.models.note import NoteCreate, NoteRead, NoteUpdate
from app.services.note_service import NoteService
from app.api.deps import CurrentUser, DBSession

router = APIRouter(prefix="/notes", tags=["notes"])

@router.get("/", response_model=List[NoteRead], status_code=status.HTTP_200_OK)
def list_notes(db: DBSession, user: CurrentUser):
    service = NoteService(db)
    return service.list_visible_notes(user.id)

@router.post("/", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
def create_note(db: DBSession, user: CurrentUser, note: NoteCreate):
    service = NoteService(db)
    return service.create(user.id, note)

@router.patch("/{note_id}", response_model=NoteRead, status_code=status.HTTP_200_OK)
def update_note(db: DBSession, user: CurrentUser, note_id: int, note: NoteUpdate):
    service = NoteService(db)
    return service.update(user.id, note_id, note)

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(db: DBSession, user: CurrentUser, note_id: int):
    service = NoteService(db)
    service.delete(user.id, note_id)
    return None