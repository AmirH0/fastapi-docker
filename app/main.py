from fastapi import FastAPI
from app.routers import auth, post, comment
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Music App")

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(comment.router)


@app.get("/")
def home():
    return {"home"}


app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://127.0.0.1:8000"],\
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
