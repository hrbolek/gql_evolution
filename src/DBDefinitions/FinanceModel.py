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

    price: Mapped[float] = mapped_column(default=0.0, nullable=True, comment="Price associated with the finance record")
    currency: Mapped[str] = mapped_column(default="CZK", nullable=True, comment="Currency of the price")
    transaction_date: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True, comment="Date of the transaction")

    # Foreign Keys
    project_id: Mapped[IDType] = UUIDFKey(nullable=False, comment="Reference to the project")
    milestone_id: Mapped[IDType] = UUIDFKey(nullable=True, comment="Reference to the milestone ")
    
    # Relationships
    project = relationship(
        "ProjectModel",
        back_populates="finances",
        uselist=False,
        foreign_keys=[project_id],
        comment="The project this finance record belongs to"
    )
    
    milestone = relationship(
        "MilestoneModel",
        back_populates="finances",
        uselist=False,
        foreign_keys=[milestone_id],
        comment="The milestone this finance record is associated with (optional)"
    )
