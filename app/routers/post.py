from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.posts import Post
from app.schemas.post import Postcreate, PostOut
from app.core.deps import getcurrentuser
from app.core.redis import r
import json

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=PostOut)
def creat_posts(
    post: Postcreate,
    db: Session = Depends(get_db),
    current_user=Depends(getcurrentuser),
):
    newpost = Post(
        title=post.title,
        content=post.content,
        slug=post.slug,
        author_id=current_user.id,
    )
    db.add(newpost)
    db.commit()
    db.refresh(newpost)
    return newpost


@router.get("/", response_model=list[PostOut])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts


@router.get("/{post_id}", response_model=PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    cached = r.get(f"post:{post_id}")
    if cached:
        return json.loads(cached)

    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404)

    r.set(
        f"post:{post_id}", json.dumps(PostOut.model_validate(post).model_dump()), ex=60
    )

    return PostOut.model_validate(post)


@router.put("/{post_id}", response_model=PostOut)
def update_post(
    post_id: int,
    updated_post: Postcreate,
    db: Session = Depends(get_db),
    current_user=Depends(getcurrentuser),
):
    post_query = db.query(Post).filter(Post.id == post_id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=404, detail="پست پیدا نشد")

    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="مجوز ندارید")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


@router.delete("/{post_id}")
def delete_post(
    post_id: int, db: Session = Depends(get_db), current_user=Depends(getcurrentuser)
):
    get_post = db.query(Post).filter(Post.id == post_id)
    fisrt = get_post.first()
    if not fisrt or fisrt.author_id != current_user.id:
        raise HTTPException(status_code=404, detail="پست موجود نیست")

    get_post.delete(synchronize_session=False)
    db.commit()
    return
