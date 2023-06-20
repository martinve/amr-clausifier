from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()


class Passage(Base):
    __tablename__ = "passages"

    id = Column(Integer, primary_key=True)
    passage = Column(String)
    rawdata = Column(String)
    context = Column(String)

    sentences = relationship("Sentence")

    def __repr__(self):
        return f"<Passage id={self.id} text={self.passage}>"


class Sentence(Base):
    __tablename__ = "sentences"

    id = Column(Integer, primary_key=True)
    passage_id = Column(Integer, ForeignKey("passages.id"))
    text = Column(String)
    parse_amr = Column(String)
    parse_ud = Column(String)
    parse_ud_raw = Column(String)
    context = Column(String)
    logic = Column(String)
    simpl_logic = Column(String)

    experiment = relationship("Passage", back_populates="sentences")

    def __repr__(self):
        return f"<Sentence id={self.id} passage_id={self.passage_id} text={self.text} logic={self.logic}>"
