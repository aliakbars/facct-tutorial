from datetime import datetime
from typing import List, Dict, Optional

from sqlmodel import SQLModel, Field, Relationship, Column, JSON

class HitsBase(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    prolific_id: str
    affiliation_country_1_1: str
    affiliation_country_1_2: Optional[str] = None
    affiliation_country_1_3: Optional[str] = None
    affiliation_country_1_4: Optional[str] = None
    affiliation_country_1_5: Optional[str] = None
    affiliation_country_2_1: str
    affiliation_country_2_2: Optional[str] = None
    affiliation_country_2_3: Optional[str] = None
    affiliation_country_2_4: Optional[str] = None
    affiliation_country_2_5: Optional[str] = None
    affiliation_country_3_1: str
    affiliation_country_3_2: Optional[str] = None
    affiliation_country_3_3: Optional[str] = None
    affiliation_country_3_4: Optional[str] = None
    affiliation_country_3_5: Optional[str] = None
    affiliation_country_4_1: str
    affiliation_country_4_2: Optional[str] = None
    affiliation_country_4_3: Optional[str] = None
    affiliation_country_4_4: Optional[str] = None
    affiliation_country_4_5: Optional[str] = None
    affiliation_country_5_1: str
    affiliation_country_5_2: Optional[str] = None
    affiliation_country_5_3: Optional[str] = None
    affiliation_country_5_4: Optional[str] = None
    affiliation_country_5_5: Optional[str] = None
    author_email_1: Optional[str] = None
    author_email_2: Optional[str] = None
    author_email_3: Optional[str] = None
    author_email_4: Optional[str] = None
    author_email_5: Optional[str] = None
    dataset_name_1: Optional[str] = None
    dataset_name_2: Optional[str] = None
    dataset_name_3: Optional[str] = None
    dataset_name_4: Optional[str] = None
    dataset_name_5: Optional[str] = None
    nb_authors_1_1: int
    nb_authors_1_2: Optional[int] = None
    nb_authors_1_3: Optional[int] = None
    nb_authors_1_4: Optional[int] = None
    nb_authors_1_5: Optional[int] = None
    nb_authors_2_1: int
    nb_authors_2_2: Optional[int] = None
    nb_authors_2_3: Optional[int] = None
    nb_authors_2_4: Optional[int] = None
    nb_authors_2_5: Optional[int] = None
    nb_authors_3_1: int
    nb_authors_3_2: Optional[int] = None
    nb_authors_3_3: Optional[int] = None
    nb_authors_3_4: Optional[int] = None
    nb_authors_3_5: Optional[int] = None
    nb_authors_4_1: int
    nb_authors_4_2: Optional[int] = None
    nb_authors_4_3: Optional[int] = None
    nb_authors_4_4: Optional[int] = None
    nb_authors_4_5: Optional[int] = None
    nb_authors_5_1: int
    nb_authors_5_2: Optional[int] = None
    nb_authors_5_3: Optional[int] = None
    nb_authors_5_4: Optional[int] = None
    nb_authors_5_5: Optional[int] = None
    nb_participants_1_1: int
    nb_participants_1_2: Optional[int] = None
    nb_participants_1_3: Optional[int] = None
    nb_participants_1_4: Optional[int] = None
    nb_participants_1_5: Optional[int] = None
    nb_participants_2_1: int
    nb_participants_2_2: Optional[int] = None
    nb_participants_2_3: Optional[int] = None
    nb_participants_2_4: Optional[int] = None
    nb_participants_2_5: Optional[int] = None
    nb_participants_3_1: int
    nb_participants_3_2: Optional[int] = None
    nb_participants_3_3: Optional[int] = None
    nb_participants_3_4: Optional[int] = None
    nb_participants_3_5: Optional[int] = None
    nb_participants_4_1: int
    nb_participants_4_2: Optional[int] = None
    nb_participants_4_3: Optional[int] = None
    nb_participants_4_4: Optional[int] = None
    nb_participants_4_5: Optional[int] = None
    nb_participants_5_1: int
    nb_participants_5_2: Optional[int] = None
    nb_participants_5_3: Optional[int] = None
    nb_participants_5_4: Optional[int] = None
    nb_participants_5_5: Optional[int] = None
    origin_1: str
    origin_2: str
    origin_3: str
    origin_4: str
    origin_5: str
    paper_url_1: str
    paper_url_2: str
    paper_url_3: str
    paper_url_4: str
    paper_url_5: str
    participant_country_1_1: str
    participant_country_1_2: Optional[str] = None
    participant_country_1_3: Optional[str] = None
    participant_country_1_4: Optional[str] = None
    participant_country_1_5: Optional[str] = None
    participant_country_2_1: str
    participant_country_2_2: Optional[str] = None
    participant_country_2_3: Optional[str] = None
    participant_country_2_4: Optional[str] = None
    participant_country_2_5: Optional[str] = None
    participant_country_3_1: str
    participant_country_3_2: Optional[str] = None
    participant_country_3_3: Optional[str] = None
    participant_country_3_4: Optional[str] = None
    participant_country_3_5: Optional[str] = None
    participant_country_4_1: str
    participant_country_4_2: Optional[str] = None
    participant_country_4_3: Optional[str] = None
    participant_country_4_4: Optional[str] = None
    participant_country_4_5: Optional[str] = None
    participant_country_5_1: str
    participant_country_5_2: Optional[str] = None
    participant_country_5_3: Optional[str] = None
    participant_country_5_4: Optional[str] = None
    participant_country_5_5: Optional[str] = None
    subject_type_1: str
    subject_type_2: str
    subject_type_3: str
    subject_type_4: str
    subject_type_5: str
    url_1: Optional[str] = None
    url_2: Optional[str] = None
    url_3: Optional[str] = None
    url_4: Optional[str] = None
    url_5: Optional[str] = None
    check_1: str
    check_2: str

class Annotator(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    prolific_id: str
    study_id: str
    session_id: str
    created_at: datetime = Field(default=datetime.now())

class Paper(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str
    locked: bool = Field(default=False)
    locked_by: Optional[int] = Field(default=None, foreign_key="annotator.id")
    lock_time: Optional[datetime] = Field(default=None)

def lock(paper: Paper, locked_by: int):
    paper.locked = True
    paper.locked_by = locked_by
    paper.lock_time = datetime.now()
    return paper

def unlock(paper: Paper):
    paper.locked = False
    paper.locked_by = None
    paper.lock_time = None
    return paper

class Annotation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    paper_id: int = Field(foreign_key="paper.id")
    annotator_id: int = Field(foreign_key="annotator.id")
    attention_check: str
    author_email: Optional[str] = Field(default=None)
    variables: Dict = Field(default={}, sa_column=Column(JSON))
    is_valid: Optional[bool] = Field(default=None)
    created_at: datetime = Field(default=datetime.now())