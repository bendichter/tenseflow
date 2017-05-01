from sqlalchemy import Column, String
from tenseflow.database import Base

MAX_LEN = 1000


class Answer(Base):
    __tablename__ = 'answers'
    text_in = Column(String(MAX_LEN), primary_key=True)
    text_out = Column(String(MAX_LEN), unique=True)
    correction = Column(String(MAX_LEN), unique=True)

    def __init__(self, text_in=None, tense=None, text_out=None, correction=None):
        self.text_in = text_in
        self.tense = tense
        self.text_out = text_out
        self.correction = correction

    def __repr__(self):
        return self.text_in