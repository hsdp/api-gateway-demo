import os
import requests
from random_words import LoremIpsum
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, create_session
from sqlalchemy.ext.declarative import declarative_base
from factories.log import create_logger
from config import Config


config = Config()
engine = create_engine(config.DB_URI, echo=False)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
ModelBase = declarative_base(name='Model')
ModelBase.query = db_session.query_property()


def init_db():
    import models
    ModelBase.metadata.create_all(bind=engine)
    log = create_logger('users-api-initdb')

    def create_users():
        word_url = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
        log.info("Getting words for random names...")
        words = requests.get(word_url).text.splitlines()
        upper_words = [word for word in words if word[0].isupper()]
        name_words = [word.lower() for word in upper_words if not word.isupper()]
        li = LoremIpsum()
        for name in name_words:
            u = models.Users(name=name, comments=[li.get_sentences(5) for i in range(10)])
            db_session.add(u)
        db_session.commit()
        del upper_words
        del name_words

    if not models.Users.query.all():
        log.info("Seeding new database with test data...")
        create_users()
        log.info("Successfully seeded database!")
