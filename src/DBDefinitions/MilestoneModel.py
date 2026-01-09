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
class MilestoneModel(BaseModel):
    __tablename__ = "Milestone_evolution"

    name: Mapped[str] = mapped_column(default=None, nullable=True, comment="Name of the project")
    description: Mapped[str] = mapped_column(default=None, nullable=True, comment="Description of the project")
    duedate: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True, comment="Due date of the milestone")
    iscompleted: Mapped[bool] = mapped_column(default=False, nullable=False, comment="Is the milestone completed?")
    
    # Foreign Key to Project
    project_id: Mapped[IDType] = UUIDFKey(nullable=False, comment="Reference to the project")
    
    # Relationship back to Project
    project = relationship(
        "ProjectModel",
        back_populates="milestones",
        uselist=False,
        foreign_keys=[project_id],
        comment="The project this milestone belongs to"
    )
    
    # Relationship to Finance
    finances = relationship(
        "FinanceModel",
        back_populates="milestone",
        uselist=True,
        cascade="save-update, delete",
        comment="Financial records associated with this milestone"
    )