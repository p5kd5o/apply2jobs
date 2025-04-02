from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

api = FastAPI(
    title="apply2jobs"
)

ORIGINS_REGEX = r"https?://localhost(:\d+)?"
api.add_middleware(
    CORSMiddleware,
    allow_origin_regex=ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
