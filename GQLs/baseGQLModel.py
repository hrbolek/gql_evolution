import uuid
import strawberry
import typing
import datetime as dt
import dataclasses
from uoishelpers.gqlpermissions import OnlyForAuthentized, RBACObjectGQLModel

# Lazy annotation for the UserGQLModel to avoid circular imports
UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".UserGQLModel")]

@strawberry.interface(description="Base interface for all GQL models")
class BaseGQLModel:
    # Define how table resolvers should be implemented in subclasses
    @classmethod
    def get_table_resolvers(cls):
        raise NotImplementedError()

    # Define how to get a data loader for database queries
    @classmethod
    def getloader(cls, info: strawberry.types.Info):
        raise NotImplementedError()
    
    # Convert a dataclass instance into a GQL model instance
    @classmethod
    def from_dataclass(cls, db_row):
        db_row_dict = dataclasses.asdict(db_row)
        instance = cls(**db_row_dict)
        return instance

    # Convert an SQLAlchemy row into a GQL model instance
    @classmethod
    def from_sqlalchemy(cls, db_row):
        keyed_resolvers = cls.get_table_resolvers()
        instance_values = {
            name: resolver(db_row)
            for name, resolver in keyed_resolvers.items()
        } if db_row is not None else {}

        instance = cls(**instance_values) if db_row is not None else None
        return instance

    # Load a single record using a data loader
    @classmethod
    async def load_with_loader(cls, info: strawberry.types.Info, id: uuid.UUID):
        loader = cls.getloader(info=info)
        db_row = await loader.load(id)
        return cls.from_sqlalchemy(db_row=db_row)
    
    # Resolve a reference by ID using a data loader
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID):
        if id is None: 
            return None
        loader = cls.getloader(info)
        if isinstance(id, str): 
            id = uuid.UUID(id)
        result = await loader.load(id)
        if result is not None:
            result.__strawberry_definition__ = cls.__strawberry_definition__
        result = cls.from_sqlalchemy(result)
        return result
    
    # Common fields for all models
    id: uuid.UUID = strawberry.field(description="Primary key", default=None, permission_classes=[OnlyForAuthentized])
    lastchange: typing.Optional[dt.datetime] = strawberry.field(description="Last change", default=None, permission_classes=[OnlyForAuthentized])
    created: typing.Optional[dt.datetime] = strawberry.field(description="Created", default=None, permission_classes=[OnlyForAuthentized])
    createdby_id: typing.Optional[uuid.UUID] = strawberry.field(description="ID of the creator", default=None, permission_classes=[OnlyForAuthentized])
    changedby_id: typing.Optional[uuid.UUID] = strawberry.field(description="ID of the last changer", default=None, permission_classes=[OnlyForAuthentized])
    rbacobject_id: typing.Optional[uuid.UUID] = strawberry.field(description="ID of the RBAC object", default=None, permission_classes=[OnlyForAuthentized])

    # Fetch the user who created this entity
    @strawberry.field(
        description="Who created this entity",
        permission_classes=[OnlyForAuthentized]
    )
    async def createdby(self) -> typing.Optional["UserGQLModel"]:
        from .UserGQLModel import UserGQLModel
        return None if self.createdby_id is None else UserGQLModel(id=self.createdby_id)

    # Fetch the user who last modified this entity
    @strawberry.field(
        description="Who last changed this entity",
        permission_classes=[OnlyForAuthentized]
    )
    async def changedby(self) -> typing.Optional["UserGQLModel"]:
        from .UserGQLModel import UserGQLModel
        return None if self.changedby_id is None else UserGQLModel(id=self.changedby_id)
    
    # Fetch the RBAC object related to this entity
    @strawberry.field(
        description="RBAC holds relations of user",
        permission_classes=[OnlyForAuthentized]
    )
    async def rbacobject(self) -> typing.Optional["RBACObjectGQLModel"]:
        return None if self.rbacobject_id is None else RBACObjectGQLModel(id=self.rbacobject_id)
