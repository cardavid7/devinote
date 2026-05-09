from fastapi import APIRouter, status
from typing import List
from app.models.label import LabelCreate, LabelRead
from app.api.deps import CurrentUser, DBSession
from app.services.label_service import LabelService

router = APIRouter(prefix="/labels", tags=["labels"])

@router.get("/", response_model=List[LabelRead], status_code=status.HTTP_200_OK)
def list_labels(db: DBSession, user: CurrentUser):
    service = LabelService(db)
    return service.list(user.id)

@router.post("/", response_model=LabelRead, status_code=status.HTTP_201_CREATED)
def create_label(db: DBSession, user: CurrentUser, label: LabelCreate):
    service = LabelService(db)
    return service.create(user.id, label)

@router.delete("/{label_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_label(db: DBSession, user: CurrentUser, label_id: int):
    service = LabelService(db)
    service.delete(user.id, label_id)
    return None