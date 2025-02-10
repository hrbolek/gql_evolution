import datetime
import uuid
import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from .BaseDBModel import BaseModel, UUIDFKey, UUIDColumn

class DisciplineModel(BaseModel):
    """Represents a discipline in the system."""

    __tablename__ = "tv_disciplines"

    summary_id: Mapped[uuid.UUID] = UUIDFKey(
        "tv_summaries.id",
        nullable=True,
        default=None,
        comment="ID of the related summary"
    )

    name: Mapped[str] = mapped_column(
        nullable=False,
        default="",
        comment="Name of the discipline"
    )
    name_en: Mapped[str] = mapped_column(
        nullable=True,
        default=None,
        comment="Name of the discipline in English"
    )
    description: Mapped[str] = mapped_column(
        nullable=True,
        default=None,
        comment="Description of the discipline"
    )

    summary = relationship(
        "SummaryModel",
        back_populates="disciplines"
    )

class DisciplineSetModel(BaseModel):
    """Represents a set of disciplines."""

    __tablename__ = "tv_discipline_sets"

    summary_id: Mapped[uuid.UUID] = UUIDFKey(
        "tv_summaries.id",
        nullable=True,
        default=None,
        comment="ID of the related summary"
    )

    name: Mapped[str] = mapped_column(
        nullable=False,
        default="",
        comment="Name of the discipline set"
    )
    name_en: Mapped[str] = mapped_column(
        nullable=True,
        default=None,
        comment="Name of the discipline set in English"
    )
    description: Mapped[str] = mapped_column(
        nullable=True,
        default=None,
        comment="Description of the discipline set"
    )
    minimum_points: Mapped[int] = mapped_column(
        nullable=True,
        default=None,
        comment="Minimum points required"
    )

    summary = relationship(
        "SummaryModel",
        back_populates="sets"
    )

class SummaryModel(BaseModel):
    """Represents a summary of disciplines and sets."""

    __tablename__ = "tv_summaries"

    result_id: Mapped[uuid.UUID] = UUIDFKey(
        "tv_results.id",
        nullable=True,
        default=None,
        comment="ID of the related result"
    )
    norm_id: Mapped[uuid.UUID] = UUIDFKey(
        "tv_norms.id",
        nullable=True,
        default=None,
        comment="ID of the related norm"
    )

    effective_date: Mapped[datetime.datetime] = mapped_column(
        nullable=True,
        default=None,
        comment="Effective date of the summary"
    )
    expiration_date: Mapped[datetime.datetime] = mapped_column(
        nullable=True,
        default=None,
        comment="Expiration date of the summary"
    )
    point_range: Mapped[str] = mapped_column(
        nullable=False,
        default="",
        comment="Range of points"
    )

    disciplines = relationship(
        "DisciplineModel",
        back_populates="summary"
    )
    sets = relationship(
        "DisciplineSetModel",
        back_populates="summary"
    )
    result = relationship(
        "ResultModel",
        back_populates="summaries"
    )
    norm = relationship(
        "NormModel",
        back_populates="summaries"
    )

class ResultModel(BaseModel):
    """Represents a test result."""

    __tablename__ = "tv_results"

    tested_person_id: Mapped[uuid.UUID] = UUIDFKey(
        nullable=True,
        default=None,
        comment="ID of the tested person"
    )
    examiner_person_id: Mapped[uuid.UUID] = UUIDFKey(
        nullable=True,
        default=None,
        comment="ID of the examiner"
    )

    evaluation_date: Mapped[datetime.datetime] = mapped_column(
        nullable=True,
        default=None,
        comment="Date and time of the evaluation"
    )
    result: Mapped[str] = mapped_column(
        nullable=False,
        default="",
        comment="Result of the test"
    )
    note: Mapped[str] = mapped_column(
        nullable=True,
        default=None,
        comment="Additional notes"
    )

    summaries = relationship(
        "SummaryModel",
        back_populates="result"
    )

class NormModel(BaseModel):
    """Represents a norm for test results."""

    __tablename__ = "tv_norms"

    effective_date: Mapped[datetime.datetime] = mapped_column(
        nullable=True,
        default=None,
        comment="Effective date of the norm"
    )
    expiration_date: Mapped[datetime.datetime] = mapped_column(
        nullable=True,
        default=None,
        comment="Expiration date of the norm"
    )
    male: Mapped[bool] = mapped_column(
        nullable=True,
        default=False,
        comment="Indicates if the norm is for males"
    )
    female: Mapped[bool] = mapped_column(
        nullable=True,
        default=False,
        comment="Indicates if the norm is for females"
    )
    age_minimal: Mapped[int] = mapped_column(
        nullable=True,
        default=None,
        comment="Minimum age"
    )
    age_maximal: Mapped[int] = mapped_column(
        nullable=True,
        default=None,
        comment="Maximum age"
    )
    result_minimal_value: Mapped[int] = mapped_column(
        nullable=True,
        default=None,
        comment="Minimum value for the result"
    )
    result_maximal_value: Mapped[int] = mapped_column(
        nullable=True,
        default=None,
        comment="Maximum value for the result"
    )
    points: Mapped[int] = mapped_column(
        nullable=True,
        default=None,
        comment="Points for the norm"
    )

    summaries = relationship(
        "SummaryModel",
        back_populates="norm"
    )

    @validates("male", "female")
    def validate_gender(self, key, value):
        if key == "male" and value:
            assert not self.female, "Cannot be both male and female"
        if key == "female" and value:
            assert not self.male, "Cannot be both male and female"
        return value
