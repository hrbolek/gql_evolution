import typing
import datetime
import dataclasses
import sqlalchemy
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, synonym

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, column_property

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType
from sqlalchemy.dialects.postgresql import ARRAY

###########################################################################################################################
#
# zde definujte sve SQLAlchemy modely
# je-li treba, muzete definovat modely obsahujici jen id polozku, na ktere se budete odkazovat
#
###########################################################################################################################
class ProjectModel(BaseModel):
    __tablename__ = "projects_evolution"

    name: Mapped[str] = mapped_column(default=None, nullable=True, comment="Name of the project")
    description: Mapped[str] = mapped_column(default=None, nullable=True, comment="Description of the project")
    startdate: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True, comment="Start date of the project")
    enddate: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True, comment="End date of the project")
    isdone: Mapped[bool] = mapped_column(default=False, nullable=False, comment="Is the project done?")
    
    # Relationships
    milestones = relationship(
        "MilestoneModel",
        back_populates="project",
        uselist=True,
        cascade="save-update, delete",
        comment="Milestones associated with this project"
    )
    
    finances = relationship(
        "FinanceModel",
        back_populates="project",
        uselist=True,
        cascade="save-update, delete",
        comment="Financial records associated with this project"
    )

