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
    parent_attribute_name = "masterevent"
    parent_id_attribute_name = "masterevent_id"
    children_attribute_name = "subevents"

    # Materialized path technique
    path: Mapped[str] = mapped_column(
        index=True,
        nullable=True,
        default=None,
        comment="Materialized path technique, not implemented"
    )
    
    #semantic vector, default is 1024 zeros
    vector: Mapped[typing.List[float]] = mapped_column(
        ARRAY(sqlalchemy.Float),
        nullable=True,
        default_factory=lambda: [0.0] * 1024
    )


    @hybrid_property
    def valid(self):
        """Evaluates if the entity is valid based on the current datetime."""
        now = datetime.datetime.now(datetime.timezone.utc)
        if self.startdate and self.enddate:
            return self.startdate <= now <= self.enddate
        elif self.startdate:
            return self.startdate <= now
        elif self.enddate:
            return now <= self.enddate
        return False

    @valid.expression
    def valid(cls):
        """Defines the SQL expression for the 'valid' property."""
        now = datetime.datetime.utcnow()
        return sqlalchemy.and_(
            sqlalchemy.or_(cls.startdate <= now, cls.startdate.is_(None)),  # Valid if startdate is in the past or missing
            sqlalchemy.or_(cls.enddate >= now, cls.enddate.is_(None))       # Valid if enddate is in the future or missing
        )