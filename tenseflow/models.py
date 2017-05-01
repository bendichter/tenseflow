from sqlalchemy import Column, String, Integer, Boolean
from tenseflow.database import Base

MAX_LEN = 1000


class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    text_in = Column(String(MAX_LEN))
    text_out = Column(String(MAX_LEN))
    correction = Column(String(MAX_LEN))
    incorrect = Column(Boolean)

    def __init__(self, text_in=None, tense=None, text_out=None, incorrect=False, correction=None):
        self.text_in = text_in
        self.tense = tense
        self.text_out = text_out
        self.correction = correction
        self.incorrect = incorrect

    def __repr__(self):
        return str(self.id) + ': ' + self.text_in[:10]
