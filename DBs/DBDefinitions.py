import sqlalchemy
import datetime
import json
from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    ForeignKey,
    Boolean
)
from sqlalchemy.dialects.postgresql import UUID
from .baseDBModel import BaseModel
from sqlalchemy.orm import relationship, validates
import uuid

# Helper function to generate a new UUID as a string
def newUuidAsString():
    return f"{uuid.uuid1()}"

# Function to create a UUID column with optional name
def UUIDColumn(name=None):
    if name is None:
        return Column(String, primary_key=True, unique=True, default=newUuidAsString)
    else:
        return Column(
            name, String, primary_key=True, unique=True, default=newUuidAsString
        )

# Function to create a foreign key column with UUID type
def UUIDFKey(ForeignKey=None, nullable=False, **kwargs):
    if ForeignKey is None:
        return Column(
            String, index=True, nullable=nullable, **kwargs
        )
    else:
        return Column(
            ForeignKey, index=True, nullable=nullable, **kwargs
        )

# Discipline model
class DisciplineModel(BaseModel):
    __tablename__ = "tv_disciplines"
   
    id = UUIDColumn()
    name = Column(String, comment="název disciplíny")
    nameEn = Column(String, nullable=True, comment="název disciplíny v ENG")
    description = Column(String, nullable=True, comment="popis disciplíny")

    sets = relationship("DisciplineSetModel", back_populates="disciplines")
    results = relationship("ResultModel", back_populates="discipline")
    templates = relationship("SummaryModel", back_populates="disciplines")
    norms = relationship("NormModel", back_populates="discipline")

# Discipline set model
class DisciplineSetModel(BaseModel):
    __tablename__ = "tv_discipline_sets"
   
    id = UUIDColumn()
    name = Column(String, comment="název souboru disciplín")
    nameEn = Column(String, nullable=True, comment="název souboru disciplín v ENG")
    description = Column(String, nullable=True, comment="popis souboru disciplín")
    minimumPoints = Column(Integer, nullable=True, comment="minimální počet bodů")

    disciplines = relationship("DisciplineModel", back_populates="sets")
    templates = relationship("SummaryModel", back_populates="set")

# Summary model
class SummaryModel(BaseModel):
    __tablename__ = "tv_result_templates"
   
    id = UUIDColumn()
    discipline_id = UUIDFKey(ForeignKey("tv_disciplines.id"), comment="id disciplíny")
    discipline_set_id = UUIDFKey(ForeignKey("tv_discipline_sets.id"), comment="id souboru disciplín")
    effective_date = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="datum účinnosti")
    expiration_date = Column(DateTime, nullable=True, comment="datum zániku")
    point_range = Column(String, comment="rozsah bodů")
    point_type = Column(String, comment="typ bodů")

    disciplines = relationship("DisciplineModel", back_populates="templates")
    set = relationship("DisciplineSetModel", back_populates="templates")
    results = relationship("ResultModel", back_populates="template")
    norms = relationship("NormModel", back_populates="template")

# Result model
class ResultModel(BaseModel):
    __tablename__ = "tv_results"

    id = UUIDColumn()
    tested_person_id = UUIDFKey(comment="id testované osoby")
    examiner_person_id = UUIDFKey(comment="id zkoušející osoby")
    discipline_id = UUIDFKey(ForeignKey("tv_disciplines.id"), comment="id disciplíny")
    datetime = Column(DateTime, comment="datum a čas výsledku")
    result = Column(String, comment="výsledek")
    note = Column(String, nullable=True, comment="poznámka")

    testedPerson = relationship("UserModel", foreign_keys=[tested_person_id])
    examinerPerson = relationship("UserModel", foreign_keys=[examiner_person_id])
    discipline = relationship("DisciplineModel", back_populates="results")
    template = relationship("SummaryModel", back_populates="results")
    norm = relationship("NormModel", back_populates="results")

# Norm model
class NormModel(BaseModel):
    __tablename__ = "tv_norms"

    id = UUIDColumn()
    discipline_set_id = UUIDFKey(ForeignKey("tv_discipline_sets.id"), comment="id souboru disciplín")
    effective_date = Column(DateTime, comment="datum účinnosti")
    expiry_date = Column(DateTime, nullable=True, comment="datum zániku")
    male = Column(Boolean, default=False, comment="muž")
    female = Column(Boolean, default=False, comment="žena")
    age_minimal = Column(Integer, comment="minimální věk")
    age_maximal = Column(Integer, comment="maximální věk")
    result_minimal_value = Column(Integer, comment="minimální hodnota výsledku")
    result_maximal_value = Column(Integer, comment="maximální hodnota výsledku")
    points = Column(Integer, comment="body")

    discipline = relationship("DisciplineModel", back_populates="norms")
    results = relationship("ResultModel", back_populates="norm")
    template = relationship("SummaryModel", back_populates="norms")

    # Validation of gender by allowing only one gender to be true
    @validates('male', 'female')
    def validate_gender(self, key, value):
        if key == 'male' and value:
            assert not self.female, "nemůže být zároveň muž a žena"
        if key == 'female' and value:
            assert not self.male, "nemůže být zároveň muž a žena"
        return value