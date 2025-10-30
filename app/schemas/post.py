from pydantic import BaseModel


class Post(BaseModel):
    title: str
    content: str


class Postcreate(BaseModel):
    title: str
    slug: str
    content: str


class PostOut(BaseModel):
    id: int
    author_id: int
    title: str
    content: str

    class Config:
        from_attributes = True
