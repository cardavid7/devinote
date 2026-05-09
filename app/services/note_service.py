
from sqlmodel import Session
from fastapi import HTTPException, status
from app.models.note import Note, NoteCreate, NoteUpdate
from app.models.share import ShareRole
from app.repositories.label_repository import LabelRepository
from app.repositories.note_repository import NoteRepository
from app.repositories.share_repository import ShareRepository


class NoteService:
    def __init__(self, db: Session):
        self.db = db
        self.notes = NoteRepository(db)
        self.labels = LabelRepository(db)
        self.shares = ShareRepository(db)

    #Permission helper
    def user_can_read(self, user_id: int, note: Note) -> bool:
        if note.owner_id == user_id:
            return True

        if self.shares.has_note_share(note_id=note.id, user_id=user_id, role="read"):
            return True
        
        label_ids = self.labels.list_label_ids_for_note(note_id=note.id)
        return self.shares.has_any_label_share(label_ids=label_ids, user_id=user_id)
    
    def user_can_edit(self, user_id: int, note: Note) -> bool:
        if note.owner_id == user_id:
            return True
        
        if self.shares.has_note_share(note_id=note.id, user_id=user_id, role= ShareRole.EDIT):
            return True
        
        label_ids = self.labels.list_label_ids_for_note(note_id=note.id)
        return self.shares.has_any_label_share(label_ids=label_ids, user_id=user_id, role= ShareRole.EDIT)

    def list_visible_notes(self, user_id: int) -> list[Note]:
        all_notes = self.notes.get_all_by_owner(owner_id=user_id)

        direct_ids = self.shares.list_note_ids_shared_directly(user_id=user_id)
        shared_label_note_ids = self.shares.list_label_ids_shared_with_user(user_id=user_id)
        ids_by_label = self.labels.list_note_ids_by_label_ids(shared_label_note_ids)

        combined_ids = list({*direct_ids, *ids_by_label})
        visible_shared_notes = self.notes.list_by_ids(combined_ids)

        combined = {note.id : note for note in all_notes}
        for note in visible_shared_notes:
            combined.setdefault(note.id, note)

        return sorted(combined.values(), key= lambda note : note.id, reverse=True)
    
    def create(self, owner_id: int, note_data: NoteCreate) -> Note:
        note = self.notes.create(Note(
            owner_id = owner_id,
            **note_data.model_dump(exclude={"label_ids"})
        ))

        if note_data.label_ids:
            self._set_labels(owner_id, note.id, note_data.label_ids)
        
        return note
        
    def update(self, user_id: int, note_id: int, note_data: NoteUpdate) -> Note:
        note = self.notes.get_by_id(note_id)
        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        if not self.user_can_edit(user_id, note):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User cannot edit this note")
        
        updates = note_data.model_dump(exclude_none=True)
        label_ids = updates.pop("label_ids", None)

        for key, value in updates.items():
            setattr(note, key, value)

        note = self.notes.update(note)

        if label_ids is not None:
            if note.owner_id != user_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Only owner can update labels")
            self._set_labels(user_id, note.id, label_ids)

        return note


    def delete(self, user_id: int, note_id: int) -> None:
        note = self.notes.get_by_id(note_id)
        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        if note.owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User cannot delete this note")
        self.notes.delete(note)

    #private helper
    def _set_labels(self, owner_id: int, note_id: int, label_ids: list[int]) -> None:
        valid_ids = self.labels.list_id_for_owner_subset(owner_id=owner_id, label_ids=label_ids or [])
        self.notes.replace_labels(note_id=note_id, label_ids=valid_ids)


    
    
