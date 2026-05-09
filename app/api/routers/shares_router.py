from fastapi import APIRouter, status
from app.api.deps import CurrentUser, DBSession
from app.models.share import ShareRequest
from app.services.share_service import ShareService

router = APIRouter(prefix="/shares", tags=["shares"])

@router.post("/notes/{note_id}", status_code=status.HTTP_201_CREATED)
def share_note(db: DBSession, user: CurrentUser, note_id: int, share: ShareRequest):
    service = ShareService(db)
    share_note = service.share_note(user.id, note_id, share.target_user_id, share.role)
    return {
        "id" : share_note.id,
        "note_id": note_id,
        "target_user_id": share.target_user_id,
        "role": share_note.role
    }

@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def unshare_note(db: DBSession, user: CurrentUser, note_id: int, target_user_id: int):
    service = ShareService(db)
    service.unshare_note(user.id, note_id, target_user_id)
    return None

@router.post("/labels/{label_id}", status_code=status.HTTP_201_CREATED)
def share_label(db: DBSession, user: CurrentUser, label_id: int, share: ShareRequest):
    service = ShareService(db)
    share_label = service.share_label(user.id, label_id, share.target_user_id, share.role)
    return {
        "id" : share_label.id,
        "label_id": label_id,
        "target_user_id": share.target_user_id,
        "role": share_label.role
    }

@router.delete("/labels/{label_id}", status_code=status.HTTP_204_NO_CONTENT)
def unshare_label(db: DBSession, user: CurrentUser, label_id: int, target_user_id: int):
    service = ShareService(db)
    service.unshare_label(user.id, label_id, target_user_id)
    return None
    