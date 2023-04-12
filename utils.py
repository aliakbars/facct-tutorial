from datetime import datetime
from models import Paper, unlock
from sqlmodel import Session, SQLModel, create_engine, select

import logging
import pandas as pd
import threading
import time
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

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

CUTOFF_TIME = config["cutoff_time"]

def add_papers():
    df = pd.read_csv(config["papers_file"])
    with Session(engine) as session:
        for url in df["url"].values:
            paper = session.exec(select(Paper).where(Paper.url == url)).first()
            if not paper:
                session.add(Paper(url=url))
                session.commit()

def release_all_locks():
    with Session(engine) as session:
        for paper in session.exec(select(Paper).where(Paper.locked)):
            unlock(paper)
            session.add(paper)
            session.commit()

def release_locks_thread():
    with Session(engine) as session:
        while True:
            for paper in session.exec(select(Paper).where(Paper.locked)):
                if (datetime.now() - paper.lock_time).seconds > CUTOFF_TIME:
                    logger.info(f"Releasing the lock for paper {paper.id}")
                    unlock(paper)
                    session.add(paper)
                    session.commit()

            time.sleep(5)

if __name__ == "__main__":
    lock_thread = threading.Thread(target=release_locks_thread)
    lock_thread.start()