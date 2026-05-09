
from sqlmodel import Session

from app.models.share import ShareRole
from app.repositories.label_repository import LabelRepository
from app.repositories.note_repository import NoteRepository
from app.repositories.share_repository import ShareRepository
from fastapi import HTTPException, status


class ShareService:
    def __init__(self, db: Session):
        self.shares = ShareRepository(db)
        self.notes = NoteRepository(db)
        self.labels = LabelRepository(db)    
        
    def share_note(self, owner_id: int, note_id: int, target_user_id: int, role: ShareRole):
        note = self.notes.get_by_id(note_id)

        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        if note.owner_id != owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User cannot share this note")
        
        share = self.shares.upsert_note_share(
            note_id=note_id,
            user_id=target_user_id,
            role = role.value if hasattr(role, "value") else role
        )

        return share

    def unshare_note(self, owner_id: int, note_id: int, target_user_id: int):
        note = self.notes.get_by_id(note_id)

        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        if note.owner_id != owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User cannot unshare this note")

        self.shares.remove_note_share(note_id=note_id, user_id=target_user_id)

    def share_label(self, owner_id: int, label_id: int, target_user_id: int, role: ShareRole):
        label = self.labels.get_by_id(label_id)

        if not label:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Label not found")
        if label.owner_id != owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User cannot share this label")

        share = self.shares.upsert_label_share(
            label_id=label_id,
            user_id=target_user_id,
            role=role.value if hasattr(role, "value") else role
        )

        return share
    
    def unshare_label(self, owner_id: int, label_id: int, target_user_id: int):
        label = self.labels.get_by_id(label_id)

        if not label:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Label not found")
        if label.owner_id != owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User cannot unshare this label")

        self.shares.remove_label_share(label_id=label_id, user_id=target_user_id)