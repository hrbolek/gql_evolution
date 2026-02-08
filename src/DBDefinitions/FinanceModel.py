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
# Model pro finance, který bude obsahovat informace o financích projektu a bude mít vztah N:1 na ProjectModel
# Model obsahuje id, project_id, milestone_id, price, currency, transaction_date
#
###########################################################################################################################
class FinanceModel(BaseModel):
    __tablename__ = "finance_evolution"

    
    project_id: Mapped[typing.Optional[IDType]] = mapped_column(#Foreign Key na projekt, který bude obsahovat odkaz na projekt,
        ForeignKey("projects_evolution.id"),                    #ke kterému finance patří
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

    
    price: Mapped[typing.Optional[float]] = mapped_column( #cena spojená s finančním záznamem, která bude obsahovat desetinné číslo
        default=0.0,
        nullable=True,
        comment="Price associated with the finance record",
    )

    currency: Mapped[typing.Optional[str]] = mapped_column( #měna spojená s finančním záznamem, která bude obsahovat textový řetězec, například "CZK" nebo "USD"
        sqlalchemy.String,
        nullable=True,
        default="CZK",
        comment="Currency of the price",
    )

    transaction_date: Mapped[typing.Optional[datetime.datetime]] = mapped_column( #datum transakce spojené s finančním záznamem, které bude obsahovat datum a čas
        sqlalchemy.DateTime,
        nullable=True,
        default=None,
        comment="Date of the transaction",
    )

    # vztah N:1 na ProjectModel, který bude obsahovat odkaz na projekt, ke kterému finance patří
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
