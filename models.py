from typing import List, Optional

from sqlmodel import SQLModel, Field, Relationship

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

class StudyBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    affiliation: str
    country: str
    nb_authors: int

class DatasetBase(SQLModel):
    name: str
    is_human: bool
    is_off_the_shelf: bool
    url: str

class ParticipantBase(SQLModel):
    country: str
    frequency: int
    dataset_id: Optional[int] = Field(default=None, foreign_key="dataset.id")

class Dataset(DatasetBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    participants: List["Participant"] = Relationship(back_populates="dataset")

class DatasetCreate(DatasetBase):
    pass

class DatasetRead(DatasetBase):
    id: int

class Participant(ParticipantBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    dataset: Optional[Dataset] = Relationship(back_populates="participants")

class ParticipantCreate(ParticipantBase):
    pass

class ParticipantRead(ParticipantBase):
    id: int

class ParticipantReadWithDataset(ParticipantRead):
    dataset: Optional[ParticipantRead] = None

class DatasetReadWithParticipants(DatasetRead):
    participants: List[Participant] = []