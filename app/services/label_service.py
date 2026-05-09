
from fastapi import HTTPException, status
from sqlmodel import Session

from app.models.label import Label, LabelCreate
from app.repositories.label_repository import LabelRepository


class LabelService:
    def __init__(self, db: Session):
        self.labels = LabelRepository(db)
        
    def list(self, owner_id: int) -> list[Label]:
        return self.labels.get_all_by_owner(owner_id=owner_id)

    def create(self, owner_id: int, label: LabelCreate) -> Label:
        exists_label = self.labels.get_by_name(label.name, owner_id)
        if exists_label:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Label already exists")
        return self.labels.create(owner_id=owner_id, name=label.name)
    
    def delete(self, owner_id: int, label_id: int):
        label = self.labels.get_by_id(label_id)
        if not label:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Label not found")
        if label.owner_id != owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User cannot delete this label")
        self.labels.delete(label)


    