import uuid
import strawberry
import typing
import datetime as dt
import dataclasses
from uoishelpers.gqlpermissions import OnlyForAuthentized, RBACObjectGQLModel

UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".UserGQLModel")]

@strawberry.interface(description="Base interface for all GQL models")
class BaseGQLModel:
    @classmethod
    def get_table_resolvers(cls):
        raise NotImplementedError()

    @classmethod
    def getloader(cls, info: strawberry.types.Info):
        raise NotImplementedError()
    
    @classmethod
    def from_dataclass(cls, db_row):
        db_row_dict = dataclasses.asdict(db_row)
        instance = cls(**db_row_dict)
        return instance

    @classmethod
    def from_sqlalchemy(cls, db_row):
        keyed_resolvers = cls.get_table_resolvers()
        instance_values = {
            name: resolver(db_row)
            for name, resolver in keyed_resolvers.items()
        } if db_row is not None else {}

        instance = cls(**instance_values) if db_row is not None else None
        return instance

    @classmethod
    async def load_with_loader(cls, info: strawberry.types.Info, id: uuid.UUID):
        loader = cls.getloader(info=info)
        db_row = await loader.load(id)
        return cls.from_sqlalchemy(db_row=db_row)
    
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID):
        if id is None: return None
        loader = cls.getloader(info)
        if isinstance(id, str): id = uuid.UUID(id)
        result = await loader.load(id)
        if result is not None:
            result.__strawberry_definition__ = cls.__strawberry_definition__
        result = cls.from_sqlalchemy(result)
        return result
    

    id: typing.Optional[uuid.UUID] = strawberry.field(description="Primary key", default = None, permission_classes= [OnlyForAuthentized])
    lastchange: typing.Optional[dt.datetime] = strawberry.field(description="Last change", default = None, permission_classes= [OnlyForAuthentized])
    created: typing.Optional[dt.datetime] = strawberry.field(description="Created", default = None, permission_classes= [OnlyForAuthentized])
    createdby_id: typing.Optional[uuid.UUID] = strawberry.field(description="ID of the creator", default = None, permission_classes= [OnlyForAuthentized])
    changedby_id: typing.Optional[uuid.UUID]= strawberry.field(description="ID of the last changer", default = None, permission_classes= [OnlyForAuthentized])
    rbacobject_id: typing.Optional[uuid.UUID] = strawberry.field(description="ID of the RBA object", default = None, permission_classes= [OnlyForAuthentized])

    @strawberry.field(
        description="who created this entity",
        permission_classes=[OnlyForAuthentized]
    )
    async def createdby(self) -> typing.Optional["UserGQLModel"]:
        from .UserGQLModel import UserGQLModel
        return None if self.changedby_id is None else UserGQLModel(id=self.createdby_id)

    @strawberry.field(
        description="who created this entity",
        permission_classes=[OnlyForAuthentized]
        )
    async def changedby(self) -> typing.Optional["UserGQLModel"]:
        from .UserGQLModel import UserGQLModel
        return None if self.changedby_id is None else UserGQLModel(id=self.changedby_id)
    
    @strawberry.field(
        description="rbac holds relations of user",
        permission_classes=[OnlyForAuthentized]
        )
    async def rbacobject(self) -> typing.Optional["RBACObjectGQLModel"]:
        return None if self.rbacobject_id is None else RBACObjectGQLModel(id=self.rbacobject_id)