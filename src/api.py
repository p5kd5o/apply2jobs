from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

api = FastAPI(
    title="apply2jobs"
)

origins_regex = [
    r"https?://localhost(:\d+)?",
]
api.add_middleware(
    CORSMiddleware,
    allow_origin_regex=origins_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@api.get("/")
async def root():
    return {"message": "Hello World"}
