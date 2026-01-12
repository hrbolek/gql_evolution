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
    path_attribute_name = "path"

    # Foreign Key to Project (must be declared before defaulted fields for dataclasses)
    project_id: Mapped[typing.Optional[IDType]] = mapped_column(
        ForeignKey("projects_evolution.id"),
        nullable=False,
        default=None,
        comment="Reference to the project",
    )

    # title / brief description
    name: Mapped[typing.Optional[str]] = mapped_column(
        sqlalchemy.String,
        nullable=True,
        default=None,
        comment="Name of the milestone",
    )

    description: Mapped[typing.Optional[str]] = mapped_column(
        sqlalchemy.String,
        nullable=True,
        default=None,
        comment="Description of the milestone",
    )

    duedate: Mapped[typing.Optional[datetime.datetime]] = mapped_column(
        sqlalchemy.DateTime,
        nullable=True,
        default=None,
        comment="Due date of the milestone",
    )

    iscompleted: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
        comment="Is the milestone completed?",
    )

    # Relationship back to Project
    project = relationship(
        "ProjectModel",
        back_populates="milestones",
        uselist=False,
        foreign_keys=[project_id],
    )

    # Relationship to Finance
    finances = relationship(
        "FinanceModel",
        back_populates="milestone",
        uselist=True,
        init=True,
        cascade="save-update, delete",
    )