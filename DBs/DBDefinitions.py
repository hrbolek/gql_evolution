import sqlalchemy
import datetime
import json
from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    ForeignKey,
    Boolean,
    UUID
)
# from sqlalchemy.dialects.postgresql import UUID
from .BaseDBModel import BaseModel
from sqlalchemy.orm import relationship, validates
import uuid

# Helper function to generate a new UUID as a string
def newUuidAsString():
    return f"{uuid.uuid1()}"

# Function to create a UUID column with optional name
def UUIDColumn(name=None):
    if name is None:
        return Column(UUID, primary_key=True, unique=True, default=uuid.uuid4)
    else:
        return Column(
            name, UUID, primary_key=True, unique=True, default=uuid.uuid4
        )

# Function to create a foreign key column with UUID type
def UUIDFKey(ForeignKey=None, nullable=False, **kwargs):
    if ForeignKey is None:
        return Column(
            UUID, index=True, nullable=nullable, **kwargs
        )
    else:
        return Column(
            ForeignKey, index=True, nullable=nullable, **kwargs
        )

# Discipline model
class DisciplineModel(BaseModel):
    __tablename__ = "tv_disciplines"
   
    id = UUIDColumn()
    summary_id = UUIDFKey(ForeignKey("tv_summaries.id"), comment="id sumáře")
    name = Column(String, comment="název disciplíny")
    name_en = Column(String, nullable=True, comment="název disciplíny v ENG")
    description = Column(String, nullable=True, comment="popis disciplíny")

    summary = relationship("SummaryModel", foreign_keys=[], back_populates="disciplines")

# Discipline set model
class DisciplineSetModel(BaseModel):
    __tablename__ = "tv_discipline_sets"
   
    id = UUIDColumn()
    summary_id = Column(ForeignKey("tv_summaries.id"), comment="id sumáře")
    name = Column(String, comment="název souboru disciplín")
    name_en = Column(String, nullable=True, comment="název souboru disciplín v ENG")
    description = Column(String, nullable=True, comment="popis souboru disciplín")
    minimum_points = Column(Integer, nullable=True, comment="minimální počet bodů")

    summary = relationship("SummaryModel", back_populates="sets")

# Summary model
class SummaryModel(BaseModel):
    __tablename__ = "tv_summaries"
   
    id = UUIDColumn()
    result_id = UUIDFKey(ForeignKey("tv_results.id"), comment="id výsledku")
    norm_id = UUIDFKey(ForeignKey("tv_norms.id"), comment="id normy")
    effective_date = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="datum účinnosti")
    expiration_date = Column(DateTime, nullable=True, comment="datum zániku")
    point_range = Column(String, comment="rozsah bodů")
    point_type = Column(String, comment="typ bodů")

    disciplines = relationship("DisciplineModel", back_populates="summary")
    sets = relationship("DisciplineSetModel", back_populates="summary")
    result = relationship("ResultModel", foreign_keys=[result_id], back_populates="summaries")
    norm = relationship("NormModel", foreign_keys=[norm_id], back_populates="summaries")

# Result model
class ResultModel(BaseModel):
    __tablename__ = "tv_results"

    id = UUIDColumn()
    tested_person_id = UUIDFKey(comment="id testované osoby")
    examiner_person_id = UUIDFKey(comment="id zkoušející osoby")
    evaluation_date = Column(DateTime, comment="datum a čas výsledku")
    result = Column(String, comment="výsledek")
    note = Column(String, nullable=True, comment="poznámka")

    """testedPerson = relationship("UserModel", foreign_keys=[tested_person_id])""
    ""examinerPerson = relationship("UserModel", foreign_keys=[examiner_person_id])"""
    summaries = relationship("SummaryModel", back_populates="result")

# Norm model
class NormModel(BaseModel):
    __tablename__ = "tv_norms"

    id = UUIDColumn()
    effective_date = Column(DateTime, comment="datum účinnosti")
    expiration_date = Column(DateTime, nullable=True, comment="datum zániku")
    male = Column(Boolean, default=False, comment="muž")
    female = Column(Boolean, default=False, comment="žena")
    age_minimal = Column(Integer, comment="minimální věk")
    age_maximal = Column(Integer, comment="maximální věk")
    result_minimal_value = Column(Integer, comment="minimální hodnota výsledku")
    result_maximal_value = Column(Integer, comment="maximální hodnota výsledku")
    points = Column(Integer, comment="body")

    summaries = relationship("SummaryModel", back_populates="norm")

    # Validation of gender by allowing only one gender to be true
    @validates('male', 'female')
    def validate_gender(self, key, value):
        if key == 'male' and value:
            assert not self.female, "nemůže být zároveň muž a žena"
        if key == 'female' and value:
            assert not self.male, "nemůže být zároveň muž a žena"
        return value