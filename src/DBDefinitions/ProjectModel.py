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
    path_attribute_name = "path"

    milestones = relationship(
        "MilestoneModel",
        uselist=True,
        init=True,
        cascade="save-update, delete",
        back_populates="project",
        foreign_keys="MilestoneModel.project_id",
    )

    finances = relationship(
        "FinanceModel",
        uselist=True,
        init=True,
        cascade="save-update, delete",
        back_populates="project",
        foreign_keys="FinanceModel.project_id",
    )

    name: Mapped[typing.Optional[str]] = mapped_column(
        sqlalchemy.String,
        nullable=True,
        default=None,
        comment="Name of the project",
    )

    description: Mapped[typing.Optional[str]] = mapped_column(
        sqlalchemy.String,
        nullable=True,
        default=None,
        comment="Description of the project",
    )

    startdate: Mapped[typing.Optional[datetime.datetime]] = mapped_column(
        sqlalchemy.DateTime,
        nullable=True,
        default=None,
        comment="Start date of the project",
    )

    enddate: Mapped[typing.Optional[datetime.datetime]] = mapped_column(
        sqlalchemy.DateTime,
        nullable=True,
        default=None,
        comment="End date of the project",
    )

    isdone: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
        comment="Is the project done?",
    )
