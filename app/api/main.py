from fastapi import FastAPI
from pydantic import BaseModel
from app.models import Publication, UserProfile
from app.pipeline import run_pipeline
from app.digest.markdown import render_markdown
app = FastAPI(title="Intelligence Digest API", version="0.1.0")
class DigestRequest(BaseModel):
    publications: list[Publication]
    profile: UserProfile
    limit: int = 10
@app.get("/health")
def health(): return {"status":"ok"}
@app.post("/digest")
def digest(req: DigestRequest):
    events = run_pipeline(req.publications, req.profile, req.limit)
    return {"events":[e.model_dump() for e in events], "markdown":render_markdown(events, req.profile)}
