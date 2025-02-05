import uuid
import datetime
import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase, Mapped, mapped_column

# Helper function to generate a new UUID as a string
def newUuidAsString():
    return str(uuid.uuid1())

# Function to create a primary key UUID column
def UUIDColumn(**kwargs):
    return mapped_column(
        sqlalchemy.types.Uuid,
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        nullable=False,  # Primary keys are non-nullable
        **kwargs,
        comment="Primary key"
    )

# Function to create a foreign key column with UUID type
def UUIDFKey(ForeignKeyArg=None, **kwargs):
    # Add default values for nullable and default
    kwargs.setdefault("index", True)
    kwargs.setdefault("nullable", True)
    kwargs.setdefault("default", None)
    kwargs.setdefault("comment", "Foreign key")
    
    # Properly handle the ForeignKey argument
    if ForeignKeyArg:
        return mapped_column(
            sqlalchemy.types.Uuid,
            ForeignKey(ForeignKeyArg),  # Pass ForeignKey object directly
            **kwargs
        )
    else:
        return mapped_column(
            sqlalchemy.types.Uuid,
            **kwargs
        )

# Base model for all database models
class BaseModel(MappedAsDataclass, DeclarativeBase):
    """Base model with shared attributes for all database entities."""

    # Added default to every field
    id: Mapped[uuid.UUID] = UUIDColumn()

    created: Mapped[datetime.datetime] = mapped_column(
        sqlalchemy.DateTime,
        nullable=True,
        server_default=sqlalchemy.sql.func.now(),
        default=None,
        comment="Record creation timestamp"
    )

    lastchange: Mapped[datetime.datetime] = mapped_column(
        sqlalchemy.DateTime,
        nullable=True,
        server_default=sqlalchemy.sql.func.now(),
        onupdate=sqlalchemy.sql.func.now(),
        default=None,
        comment="Last update timestamp"
    )

    createdby_id: Mapped[uuid.UUID] = mapped_column(
        nullable=True,
        default=None,
        comment="ID of the user who created this record"
    )

    changedby_id: Mapped[uuid.UUID] = mapped_column(
        nullable=True,
        default=None,
        comment="ID of the user who last modified this record"
    )

    rbacobject_id: Mapped[uuid.UUID] = UUIDFKey(
        nullable=True,
        default=None,
        comment="ID of the related RBAC object"
    )
