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
class FinanceModel(BaseModel):
    __tablename__ = "finance_evolution"

    # Foreign Keys (declare before defaulted fields)
    project_id: Mapped[typing.Optional[IDType]] = mapped_column(
        ForeignKey("projects_evolution.id"),
        nullable=False,
        default=None,
        comment="Reference to the project",
    )

    milestone_id: Mapped[typing.Optional[IDType]] = mapped_column(
        ForeignKey("Milestone_evolution.id"),
        nullable=True,
        default=None,
        comment="Reference to the milestone",
    )

    price: Mapped[typing.Optional[float]] = mapped_column(
        default=0.0,
        nullable=True,
        comment="Price associated with the finance record",
    )

    currency: Mapped[typing.Optional[str]] = mapped_column(
        sqlalchemy.String,
        nullable=True,
        default="CZK",
        comment="Currency of the price",
    )

    transaction_date: Mapped[typing.Optional[datetime.datetime]] = mapped_column(
        sqlalchemy.DateTime,
        nullable=True,
        default=None,
        comment="Date of the transaction",
    )

    # Relationships
    project = relationship(
        "ProjectModel",
        back_populates="finances",
        uselist=False,
        foreign_keys=[project_id],
    )

    milestone = relationship(
        "MilestoneModel",
        back_populates="finances",
        uselist=False,
        foreign_keys=[milestone_id],
    )
