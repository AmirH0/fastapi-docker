from pydantic import BaseModel

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    content: str

class CommentOut(CommentBase):
    id: int
    author_id: int
    post_id: int

    class Config:
         from_attributes = True
