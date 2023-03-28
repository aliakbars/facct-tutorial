from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, SQLModel, create_engine, select
from models import *
from paper_lock import RedisPaperLock

import logging
import utils
import yaml

with open("config.yml", "r") as config_file:
    config = yaml.safe_load(config_file)

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(config["logfile"])
formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
logger.addHandler(handler)

sqlite_file_name = config["database"]
sqlite_url = f"sqlite:///{sqlite_file_name}"

CUTOFF_TIME = config["cutoff_time"]

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="static/templates")

redis_paper_lock = RedisPaperLock.get()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
async def root(request: Request, PROLIFIC_PID: str, STUDY_ID: str, SESSION_ID: str, session: Session = Depends(get_session)):
    prolific_id = PROLIFIC_PID
    study_id = STUDY_ID
    session_id = SESSION_ID

    # Check if exists
    annotator = session.exec(
        select(Annotator).where(Annotator.prolific_id == prolific_id, Annotator.study_id == study_id, Annotator.session_id == session_id)
    ).first()

    if annotator:
        if (datetime.now() - annotator.created_at).seconds > CUTOFF_TIME:
            logger.error(f"Annotator {annotator.id} exceeded the time limit")
            return {"status": "error", "message": "You have exceeded the time limit"}
        else:
            paper = session.exec(select(Paper).where(
                Paper.locked_by == annotator.id
            )).first()

            # Already has a paper and not finished
            if paper and (datetime.now() - paper.lock_time).seconds < CUTOFF_TIME:
                if config["debug"]:
                    return {
                        "paper_url": paper.url,
                        "annotator_id": annotator.id
                    }
                else:
                    return templates.TemplateResponse(
                        "wild.html",
                        {
                            "request": request,
                            "paper_url": paper.url,
                            "annotator_id": annotator.id
                        }
                    )
            else:
                # Somehow did not finish
                if config["debug"]:
                    return {"status": "error", "message": "No available papers to annotate."}
                else:
                    return templates.TemplateResponse("error.html", {"request": request})
    else:
        paper = session.exec("""
        select
            paper.id
        from
            paper
        where true
            and not locked
            and paper.id not in
                (
                    select paper_id
                    from annotation
                    where true
                        and annotation.is_valid
                        or annotation.is_valid is NULL
                )
        """).first()
        
        # additional lock from redis
        if paper and redis_paper_lock.lock(paper.id):
            # Only create an annotator if there is an available paper
            annotator = Annotator(prolific_id=prolific_id, study_id=study_id, session_id=session_id)
            session.add(annotator)
            session.commit()

            paper = session.exec(select(Paper).where(Paper.id == paper.id)).one()
            paper = lock(paper, annotator.id)

            session.add(paper)
            session.commit()
            session.refresh(paper)
            if config["debug"]:
                return {
                    "paper_url": paper.url,
                    "annotator_id": annotator.id
                }
            else:
                return templates.TemplateResponse(
                    "wild.html",
                    {
                        "request": request,
                        "paper_url": paper.url,
                        "annotator_id": annotator.id
                    }
                )
        else:
            logger.error(f"No available papers to annotate")
            if config["debug"]:
                return {"status": "error", "message": "No available papers to annotate. Please try again later."}
            else:
                return templates.TemplateResponse("error.html", {"request": request})

@app.post("/")
async def save_paper(
    *,
    request: Request,
    session: Session = Depends(get_session),
    paper_url: str = Form(...),
    annotator_id: int = Form(...),
    author_email: Optional[str] = Form(None),
    author_country: List[str] = Form(...),
    nb_authors: List[str] = Form(...),
    origin: str = Form(...),
    subject_type: str = Form(...),
    dataset_name: Optional[str] = Form(None),
    dataset_url: Optional[str] = Form(None),
    participant_country: List[str] = Form(...),
    nb_participants: List[str] = Form(...),
    in_situ_lab: bool = Form(False),
    in_situ_field: bool = Form(False),
    in_situ_crowd: bool = Form(False),
    in_situ_social: bool = Form(False),
    local: str = Form(...),
    diverse: str = Form(...),
    attention_check: str = Form(...),
):
    paper = session.exec(
        select(Paper).where(Paper.url == paper_url)
    ).first()
    # unlock from redis first, then unlock at database
    redis_paper_lock.unlock(paper.id)
    unlock(paper)
    session.commit()

    dataset = {
        "dataset_name": dataset_name,
        "dataset_url": dataset_url,
        "origin": origin,
        "subject_type": subject_type,
        "in_situ_lab": in_situ_lab,
        "in_situ_field": in_situ_field,
        "in_situ_crowd": in_situ_crowd,
        "in_situ_social": in_situ_social,
        "local": local,
        "diverse": diverse,
        "attention_check": attention_check,
        "authors": [],
        "participants": []
    }

    for country, freq in zip(author_country, nb_authors):
        if country:
            dataset["authors"].append({
                "country": country,
                "frequency": int(freq)
            })
    
    for country, freq in zip(participant_country, nb_participants):
        if country:
            dataset["participants"].append({
                "country": country,
                "frequency": int(freq)
            })

    annotation = Annotation(
        paper_id=paper.id,
        annotator_id=annotator_id,
        attention_check=attention_check,
        author_email=author_email,
        variables=dataset
    )
    session.add(annotation)
    session.commit()

    return RedirectResponse(url=config["redirect_url"], status_code=status.HTTP_303_SEE_OTHER)