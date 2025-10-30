from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import Post
from app.models.comment import Comment
from app.schemas import comments
from app.database import get_db
from app.core.deps import getcurrentuser


router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/", response_model=comments.CommentOut)
def create_comment(
    comment_n: comments.CommentCreate,
    post_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(getcurrentuser),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=401, detail="not found boyy!!!!!")

    new_comment = Comment(
        content=comment_n.content, post_id=post_id, author_id=current_user.id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment
