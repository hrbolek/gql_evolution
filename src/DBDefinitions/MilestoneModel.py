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
# 
# Model pro milestone, který bude obsahovat informace o milestonu a bude mít vztah N:1 na ProjectModel
# Model obsahuje id, project_id, name, description, duedate, iscompleted
#
###########################################################################################################################
class MilestoneModel(BaseModel):
    __tablename__ = "Milestone_evolution"
    path_attribute_name = "path"

    project_id: Mapped[typing.Optional[IDType]] = mapped_column( #Foreign Key na projekt, který bude obsahovat odkaz na projekt,
        ForeignKey("projects_evolution.id"),
        nullable=False,
        default=None,
        comment="Reference to the project",
    )

    # title / brief description
    name: Mapped[typing.Optional[str]] = mapped_column( #název milestonu, který bude obsahovat textový řetězec
        sqlalchemy.String,
        nullable=True,
        default=None,
        comment="Name of the milestone",
    )

    description: Mapped[typing.Optional[str]] = mapped_column( #popis milestonu, který bude obsahovat textový řetězec
        sqlalchemy.String,
        nullable=True,
        default=None,
        comment="Description of the milestone",
    )

    duedate: Mapped[typing.Optional[datetime.datetime]] = mapped_column( #datum splnění milestonu, které bude obsahovat datum a čas
        sqlalchemy.DateTime,
        nullable=True,
        default=None,
        comment="Due date of the milestone",
    )

    iscompleted: Mapped[bool] = mapped_column( #informace o tom, zda je mileston splněn, která bude obsahovat boolean hodnotu
        default=False,
        nullable=False,
        comment="Is the milestone completed?",
    )

    
    project = relationship( #popis vztahu N:1 mezi milestonem a projektem
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