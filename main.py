from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, SQLModel, create_engine, select

from models import *
import utils

import pandas as pd
import yaml
import uvicorn

with open("config.yml", "r") as config_file:
    config = yaml.safe_load(config_file)

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

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/paper-set")
async def paper(request: Request, PROLIFIC_PID: str, STUDY_ID: str, SESSION_ID: str, session: Session = Depends(get_session)):
    prolific_id = PROLIFIC_PID
    study_id = STUDY_ID
    session_id = SESSION_ID

    # Check if exists
    annotator = session.exec(
        select(Annotator).where(Annotator.prolific_id == prolific_id, Annotator.study_id == study_id, Annotator.session_id == session_id)
    ).first()

    if annotator:
        if (datetime.now() - annotator.created_at).seconds > CUTOFF_TIME:
            return {"status": "error", "message": "You have exceeded the time limit"}
        else:
            paper = session.exec(select(Paper).where(
                Paper.locked_by == annotator.id
            )).first()

            # Already has a paper and not finished
            if paper and (datetime.now() - paper.lock_time).seconds < CUTOFF_TIME:
                if config["debug"]:
                    return {
                        "paper_urls": eval(paper.url),
                        "paper_id": paper.id,
                        "annotator_id": annotator.id
                    }
                else:
                    return templates.TemplateResponse(
                        "index.html",
                        {
                            "request": request,
                            "paper_id": paper.id,
                            "paper_urls": eval(paper.url),
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
                    from hitsbase
                    where true
                        and hitsbase.is_valid
                        or hitsbase.is_valid is NULL
                )
        """).first()
        
        if paper:
            # Only create an annotator if there is an available paper
            annotator = Annotator(
                prolific_id=prolific_id,
                study_id=study_id,
                session_id=session_id,
                created_at=datetime.now(),
            )
            session.add(annotator)
            session.commit()

            paper = session.exec(select(Paper).where(Paper.id == paper.id)).one()
            paper = lock(paper, annotator.id)

            session.add(paper)
            session.commit()
            session.refresh(paper)
            if config["debug"]:
                return {
                    "paper_urls": eval(paper.url),
                    "paper_id": paper.id,
                    "annotator_id": annotator.id
                }
            else:
                return templates.TemplateResponse(
                    "index.html",
                    {
                        "request": request,
                        "paper_id": paper.id,
                        "paper_urls": eval(paper.url),
                        "annotator_id": annotator.id
                    }
                )
        else:
            if config["debug"]:
                return {"status": "error", "message": "No available papers to annotate. Please try again later."}
            else:
                return templates.TemplateResponse("error.html", {"request": request})

@app.post("/paper-set")
async def save_form_data(
    request: Request,
    session: Session = Depends(get_session),
    paper_id: str = Form(...),
    annotator_id: str = Form(...),
    affiliation_country_1_1: str = Form(...),
    affiliation_country_1_2: Optional[str] = Form(None),
    affiliation_country_1_3: Optional[str] = Form(None),
    affiliation_country_1_4: Optional[str] = Form(None),
    affiliation_country_1_5: Optional[str] = Form(None),
    affiliation_country_2_1: str = Form(...),
    affiliation_country_2_2: Optional[str] = Form(None),
    affiliation_country_2_3: Optional[str] = Form(None),
    affiliation_country_2_4: Optional[str] = Form(None),
    affiliation_country_2_5: Optional[str] = Form(None),
    affiliation_country_3_1: str = Form(...),
    affiliation_country_3_2: Optional[str] = Form(None),
    affiliation_country_3_3: Optional[str] = Form(None),
    affiliation_country_3_4: Optional[str] = Form(None),
    affiliation_country_3_5: Optional[str] = Form(None),
    affiliation_country_4_1: str = Form(...),
    affiliation_country_4_2: Optional[str] = Form(None),
    affiliation_country_4_3: Optional[str] = Form(None),
    affiliation_country_4_4: Optional[str] = Form(None),
    affiliation_country_4_5: Optional[str] = Form(None),
    affiliation_country_5_1: str = Form(...),
    affiliation_country_5_2: Optional[str] = Form(None),
    affiliation_country_5_3: Optional[str] = Form(None),
    affiliation_country_5_4: Optional[str] = Form(None),
    affiliation_country_5_5: Optional[str] = Form(None),
    author_email_1: Optional[str] = Form(None),
    author_email_2: Optional[str] = Form(None),
    author_email_3: Optional[str] = Form(None),
    author_email_4: Optional[str] = Form(None),
    author_email_5: Optional[str] = Form(None),
    dataset_name_1: Optional[str] = Form(None),
    dataset_name_2: Optional[str] = Form(None),
    dataset_name_3: Optional[str] = Form(None),
    dataset_name_4: Optional[str] = Form(None),
    dataset_name_5: Optional[str] = Form(None),
    nb_authors_1_1: int = Form(...),
    nb_authors_1_2: Optional[int] = Form(None),
    nb_authors_1_3: Optional[int] = Form(None),
    nb_authors_1_4: Optional[int] = Form(None),
    nb_authors_1_5: Optional[int] = Form(None),
    nb_authors_2_1: int = Form(...),
    nb_authors_2_2: Optional[int] = Form(None),
    nb_authors_2_3: Optional[int] = Form(None),
    nb_authors_2_4: Optional[int] = Form(None),
    nb_authors_2_5: Optional[int] = Form(None),
    nb_authors_3_1: int = Form(...),
    nb_authors_3_2: Optional[int] = Form(None),
    nb_authors_3_3: Optional[int] = Form(None),
    nb_authors_3_4: Optional[int] = Form(None),
    nb_authors_3_5: Optional[int] = Form(None),
    nb_authors_4_1: int = Form(...),
    nb_authors_4_2: Optional[int] = Form(None),
    nb_authors_4_3: Optional[int] = Form(None),
    nb_authors_4_4: Optional[int] = Form(None),
    nb_authors_4_5: Optional[int] = Form(None),
    nb_authors_5_1: int = Form(...),
    nb_authors_5_2: Optional[int] = Form(None),
    nb_authors_5_3: Optional[int] = Form(None),
    nb_authors_5_4: Optional[int] = Form(None),
    nb_authors_5_5: Optional[int] = Form(None),
    nb_participants_1_1: int = Form(...),
    nb_participants_1_2: Optional[int] = Form(None),
    nb_participants_1_3: Optional[int] = Form(None),
    nb_participants_1_4: Optional[int] = Form(None),
    nb_participants_1_5: Optional[int] = Form(None),
    nb_participants_2_1: int = Form(...),
    nb_participants_2_2: Optional[int] = Form(None),
    nb_participants_2_3: Optional[int] = Form(None),
    nb_participants_2_4: Optional[int] = Form(None),
    nb_participants_2_5: Optional[int] = Form(None),
    nb_participants_3_1: int = Form(...),
    nb_participants_3_2: Optional[int] = Form(None),
    nb_participants_3_3: Optional[int] = Form(None),
    nb_participants_3_4: Optional[int] = Form(None),
    nb_participants_3_5: Optional[int] = Form(None),
    nb_participants_4_1: int = Form(...),
    nb_participants_4_2: Optional[int] = Form(None),
    nb_participants_4_3: Optional[int] = Form(None),
    nb_participants_4_4: Optional[int] = Form(None),
    nb_participants_4_5: Optional[int] = Form(None),
    nb_participants_5_1: int = Form(...),
    nb_participants_5_2: Optional[int] = Form(None),
    nb_participants_5_3: Optional[int] = Form(None),
    nb_participants_5_4: Optional[int] = Form(None),
    nb_participants_5_5: Optional[int] = Form(None),
    origin_1: str = Form(...),
    origin_2: str = Form(...),
    origin_3: str = Form(...),
    origin_4: str = Form(...),
    origin_5: str = Form(...),
    paper_url_1: str = Form(...),
    paper_url_2: str = Form(...),
    paper_url_3: str = Form(...),
    paper_url_4: str = Form(...),
    paper_url_5: str = Form(...),
    participant_country_1_1: str = Form(...),
    participant_country_1_2: Optional[str] = Form(None),
    participant_country_1_3: Optional[str] = Form(None),
    participant_country_1_4: Optional[str] = Form(None),
    participant_country_1_5: Optional[str] = Form(None),
    participant_country_2_1: str = Form(...),
    participant_country_2_2: Optional[str] = Form(None),
    participant_country_2_3: Optional[str] = Form(None),
    participant_country_2_4: Optional[str] = Form(None),
    participant_country_2_5: Optional[str] = Form(None),
    participant_country_3_1: str = Form(...),
    participant_country_3_2: Optional[str] = Form(None),
    participant_country_3_3: Optional[str] = Form(None),
    participant_country_3_4: Optional[str] = Form(None),
    participant_country_3_5: Optional[str] = Form(None),
    participant_country_4_1: str = Form(...),
    participant_country_4_2: Optional[str] = Form(None),
    participant_country_4_3: Optional[str] = Form(None),
    participant_country_4_4: Optional[str] = Form(None),
    participant_country_4_5: Optional[str] = Form(None),
    participant_country_5_1: str = Form(...),
    participant_country_5_2: Optional[str] = Form(None),
    participant_country_5_3: Optional[str] = Form(None),
    participant_country_5_4: Optional[str] = Form(None),
    participant_country_5_5: Optional[str] = Form(None),
    subject_type_1: str = Form(...),
    subject_type_2: str = Form(...),
    subject_type_3: str = Form(...),
    subject_type_4: str = Form(...),
    subject_type_5: str = Form(...),
    url_1: Optional[str] = Form(None),
    url_2: Optional[str] = Form(None),
    url_3: Optional[str] = Form(None),
    url_4: Optional[str] = Form(None),
    url_5: Optional[str] = Form(None),
    check_1: str = Form(...),
    check_2: str = Form(...),
):
    hits_data = HitsBase(
        paper_id=paper_id,
        annotator_id=annotator_id,
        affiliation_country_1_1=affiliation_country_1_1,
        affiliation_country_1_2=affiliation_country_1_2,
        affiliation_country_1_3=affiliation_country_1_3,
        affiliation_country_1_4=affiliation_country_1_4,
        affiliation_country_1_5=affiliation_country_1_5,
        affiliation_country_2_1=affiliation_country_2_1,
        affiliation_country_2_2=affiliation_country_2_2,
        affiliation_country_2_3=affiliation_country_2_3,
        affiliation_country_2_4=affiliation_country_2_4,
        affiliation_country_2_5=affiliation_country_2_5,
        affiliation_country_3_1=affiliation_country_3_1,
        affiliation_country_3_2=affiliation_country_3_2,
        affiliation_country_3_3=affiliation_country_3_3,
        affiliation_country_3_4=affiliation_country_3_4,
        affiliation_country_3_5=affiliation_country_3_5,
        affiliation_country_4_1=affiliation_country_4_1,
        affiliation_country_4_2=affiliation_country_4_2,
        affiliation_country_4_3=affiliation_country_4_3,
        affiliation_country_4_4=affiliation_country_4_4,
        affiliation_country_4_5=affiliation_country_4_5,
        affiliation_country_5_1=affiliation_country_5_1,
        affiliation_country_5_2=affiliation_country_5_2,
        affiliation_country_5_3=affiliation_country_5_3,
        affiliation_country_5_4=affiliation_country_5_4,
        affiliation_country_5_5=affiliation_country_5_5,
        author_email_1=author_email_1,
        author_email_2=author_email_2,
        author_email_3=author_email_3,
        author_email_4=author_email_4,
        author_email_5=author_email_5,
        dataset_name_1=dataset_name_1,
        dataset_name_2=dataset_name_2,
        dataset_name_3=dataset_name_3,
        dataset_name_4=dataset_name_4,
        dataset_name_5=dataset_name_5,
        nb_authors_1_1=nb_authors_1_1,
        nb_authors_1_2=nb_authors_1_2,
        nb_authors_1_3=nb_authors_1_3,
        nb_authors_1_4=nb_authors_1_4,
        nb_authors_1_5=nb_authors_1_5,
        nb_authors_2_1=nb_authors_2_1,
        nb_authors_2_2=nb_authors_2_2,
        nb_authors_2_3=nb_authors_2_3,
        nb_authors_2_4=nb_authors_2_4,
        nb_authors_2_5=nb_authors_2_5,
        nb_authors_3_1=nb_authors_3_1,
        nb_authors_3_2=nb_authors_3_2,
        nb_authors_3_3=nb_authors_3_3,
        nb_authors_3_4=nb_authors_3_4,
        nb_authors_3_5=nb_authors_3_5,
        nb_authors_4_1=nb_authors_4_1,
        nb_authors_4_2=nb_authors_4_2,
        nb_authors_4_3=nb_authors_4_3,
        nb_authors_4_4=nb_authors_4_4,
        nb_authors_4_5=nb_authors_4_5,
        nb_authors_5_1=nb_authors_5_1,
        nb_authors_5_2=nb_authors_5_2,
        nb_authors_5_3=nb_authors_5_3,
        nb_authors_5_4=nb_authors_5_4,
        nb_authors_5_5=nb_authors_5_5,
        nb_participants_1_1=nb_participants_1_1,
        nb_participants_1_2=nb_participants_1_2,
        nb_participants_1_3=nb_participants_1_3,
        nb_participants_1_4=nb_participants_1_4,
        nb_participants_1_5=nb_participants_1_5,
        nb_participants_2_1=nb_participants_2_1,
        nb_participants_2_2=nb_participants_2_2,
        nb_participants_2_3=nb_participants_2_3,
        nb_participants_2_4=nb_participants_2_4,
        nb_participants_2_5=nb_participants_2_5,
        nb_participants_3_1=nb_participants_3_1,
        nb_participants_3_2=nb_participants_3_2,
        nb_participants_3_3=nb_participants_3_3,
        nb_participants_3_4=nb_participants_3_4,
        nb_participants_3_5=nb_participants_3_5,
        nb_participants_4_1=nb_participants_4_1,
        nb_participants_4_2=nb_participants_4_2,
        nb_participants_4_3=nb_participants_4_3,
        nb_participants_4_4=nb_participants_4_4,
        nb_participants_4_5=nb_participants_4_5,
        nb_participants_5_1=nb_participants_5_1,
        nb_participants_5_2=nb_participants_5_2,
        nb_participants_5_3=nb_participants_5_3,
        nb_participants_5_4=nb_participants_5_4,
        nb_participants_5_5=nb_participants_5_5,
        origin_1=origin_1,
        origin_2=origin_2,
        origin_3=origin_3,
        origin_4=origin_4,
        origin_5=origin_5,
        paper_url_1=paper_url_1,
        paper_url_2=paper_url_2,
        paper_url_3=paper_url_3,
        paper_url_4=paper_url_4,
        paper_url_5=paper_url_5,
        participant_country_1_1=participant_country_1_1,
        participant_country_1_2=participant_country_1_2,
        participant_country_1_3=participant_country_1_3,
        participant_country_1_4=participant_country_1_4,
        participant_country_1_5=participant_country_1_5,
        participant_country_2_1=participant_country_2_1,
        participant_country_2_2=participant_country_2_2,
        participant_country_2_3=participant_country_2_3,
        participant_country_2_4=participant_country_2_4,
        participant_country_2_5=participant_country_2_5,
        participant_country_3_1=participant_country_3_1,
        participant_country_3_2=participant_country_3_2,
        participant_country_3_3=participant_country_3_3,
        participant_country_3_4=participant_country_3_4,
        participant_country_3_5=participant_country_3_5,
        participant_country_4_1=participant_country_4_1,
        participant_country_4_2=participant_country_4_2,
        participant_country_4_3=participant_country_4_3,
        participant_country_4_4=participant_country_4_4,
        participant_country_4_5=participant_country_4_5,
        participant_country_5_1=participant_country_5_1,
        participant_country_5_2=participant_country_5_2,
        participant_country_5_3=participant_country_5_3,
        participant_country_5_4=participant_country_5_4,
        participant_country_5_5=participant_country_5_5,
        subject_type_1=subject_type_1,
        subject_type_2=subject_type_2,
        subject_type_3=subject_type_3,
        subject_type_4=subject_type_4,
        subject_type_5=subject_type_5,
        url_1=url_1,
        url_2=url_2,
        url_3=url_3,
        url_4=url_4,
        url_5=url_5,
        check_1=check_1,
        check_2=check_2,
        created_at=datetime.now(),
    )

    paper = session.exec(
        select(Paper).where(Paper.id == paper_id)
    ).first()
    unlock(paper)

    session.add(hits_data)
    session.commit()
    return RedirectResponse(url=config["redirect_url"], status_code=status.HTTP_303_SEE_OTHER)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=7123)