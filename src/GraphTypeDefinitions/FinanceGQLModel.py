import asyncio
import dataclasses
import datetime
import typing
import strawberry

import strawberry.types
from uoishelpers.gqlpermissions import (
    OnlyForAuthentized,
    SimpleInsertPermission, 
    SimpleUpdatePermission, 
    SimpleDeletePermission
)    
from uoishelpers.resolvers import (
    getLoadersFromInfo, 
    createInputs,
    createInputs2,

    InsertError, 
    Insert, 
    UpdateError, 
    Update, 
    DeleteError, 
    Delete,

    PageResolver,
    VectorResolver,
    ScalarResolver
)
from uoishelpers.gqlpermissions.LoadDataExtension import LoadDataExtension
from uoishelpers.gqlpermissions.RbacProviderExtension import RbacProviderExtension
from uoishelpers.gqlpermissions.RbacInsertProviderExtension import RbacInsertProviderExtension
from uoishelpers.gqlpermissions.UserRoleProviderExtension import UserRoleProviderExtension
from uoishelpers.gqlpermissions.UserAccessControlExtension import UserAccessControlExtension
from uoishelpers.gqlpermissions.UserAbsoluteAccessControlExtension import UserAbsoluteAccessControlExtension

from .BaseGQLModel import BaseGQLModel, IDType, Relation
from .TimeUnit import TimeUnit

@createInputs2
class FinanceInputFilter:
    id: IDType


@strawberry.federation.type(
    description="""Entity representing a Finance""",
    keys=["id"]
)

class FinanceGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).FinanceModel

    price: typing.Optional[float] = strawberry.field(
        description="Price associated with the finance record",
        default=None
    )

    currency: typing.Optional[str] = strawberry.field(
        description="Currency of the price",
        default="CZK"
    )

    transaction_date: typing.Optional[datetime.datetime] = strawberry.field(
        description="Date of the transaction",
        default=None
    )

    project_id: typing.Optional[IDType] = strawberry.field(
        description="Reference to the project",
        default=None
    )

    milestone_id: typing.Optional[IDType] = strawberry.field(
        description="Reference to the milestone",
        default=None
    )

@strawberry.interface(
    description="""Finance queries"""
)
class FinanceQuery:
    finance_by_id: typing.Optional[FinanceGQLModel] = strawberry.field(
        description="""get a finance by its id""",
        permission_classes=[OnlyForAuthentized],
        resolver=FinanceGQLModel.load_with_loader
    )

    finance_page: typing.List[FinanceGQLModel] = strawberry.field(
        description="""get a page of finances""",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[FinanceGQLModel](whereType=FinanceInputFilter)
    )

from uoishelpers.resolvers import TreeInputStructureMixin, InputModelMixin
@strawberry.input(
    description="""Input type for creating a Finance"""
)
class FinanceInsertGQLModel(InputModelMixin):
    getLoader = FinanceGQLModel.getLoader

    id: typing.Optional[IDType] = strawberry.field(
        description="""Finance id""",
        default=None
    )
    project_id: IDType = strawberry.field(
        description="""Project id - required"""
    )
    milestone_id: typing.Optional[IDType] = strawberry.field(
        description="""Milestone id - optional""",
        default=None
    )
    price: typing.Optional[float] = strawberry.field(
        description="Price associated with the finance record",
        default=None
    )
    currency: typing.Optional[str] = strawberry.field(
        description="Currency of the price",
        default="CZK"
    )
    transaction_date: typing.Optional[datetime.datetime] = strawberry.field(
        description="Date of the transaction",
        default=None
    )
    rbacobject_id: IDType = strawberry.field(
        description="""Definitoin of access control"""
    )
    createdby_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="""Input type for updating a Finance"""
)
class FinanceUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""Finance id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="timestamp"
    )
    price: typing.Optional[float] = strawberry.field(
        description="Price associated with the finance record",
        default=None
    )
    currency: typing.Optional[str] = strawberry.field(
        description="Currency of the price",
        default=None
    )
    transaction_date: typing.Optional[datetime.datetime] = strawberry.field(
        description="Date of the transaction",
        default=None
    )
    changedby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="""Input type for deleting a Finance"""
)
class FinanceDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""Finance id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""last change""",
    )

@strawberry.interface(
    description="""Finance mutations"""
)
class FinanceMutation:
    @strawberry.mutation(
        description="""Insert a Finance""",
        permission_classes=[
            OnlyForAuthentized
            # SimpleInsertPermission[FinanceGQLModel](roles=["administrátor"])
        ],
        extensions=[
            # UpdatePermissionCheckRoleFieldExtension[GroupGQLModel](roles=["administrátor", "personalista"]),
            UserAccessControlExtension[InsertError, FinanceGQLModel](
                roles=[
                    "plánovací administrátor", 
                    "administrátor"
                ]
            ),
            UserRoleProviderExtension[InsertError, FinanceGQLModel](),
            RbacInsertProviderExtension[InsertError, FinanceGQLModel](
                rbac_key_name="rbacobject_id"    
            ),
        ],
    )
    async def finance_insert(
        self,
        info: strawberry.Info,
        finance: FinanceInsertGQLModel,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Union[FinanceGQLModel, InsertError[FinanceGQLModel]]:
        return await Insert[FinanceGQLModel].DoItSafeWay(info=info, entity=finance)
    


    @strawberry.mutation(
        description="""Update a Finance""",
        permission_classes=[
            OnlyForAuthentized
            # SimpleUpdatePermission[FinanceGQLModel](roles=["administrátor"])
        ],
        extensions=[
            # UpdatePermissionCheckRoleFieldExtension[GroupGQLModel](roles=["administrátor", "personalista"]),
            UserAccessControlExtension[UpdateError, FinanceGQLModel](
                roles=[
                    "plánovací administrátor", 
                    # "personalista"
                ]
            ),
            UserRoleProviderExtension[UpdateError, FinanceGQLModel](),
            RbacProviderExtension[UpdateError, FinanceGQLModel](),
            LoadDataExtension[UpdateError, FinanceGQLModel]()
        ],
    )
    async def finance_update(
        self,
        info: strawberry.Info,
        finance: FinanceUpdateGQLModel
    ) -> typing.Union[FinanceGQLModel, UpdateError[FinanceGQLModel]]:
        return await Update[FinanceGQLModel].DoItSafeWay(info=info, entity=finance)
    


    @strawberry.mutation(
        description="""Delete a Finance""",
        permission_classes=[
            OnlyForAuthentized,
            # SimpleDeletePermission[FinanceGQLModel](roles=["administrátor"])
        ],
        extensions=[
            # UpdatePermissionCheckRoleFieldExtension[GroupGQLModel](roles=["administrátor", "personalista"]),
            UserAccessControlExtension[DeleteError, FinanceGQLModel](
                roles=[
                    "plánovací administrátor", 
                    # "personalista"
                ]
            ),
            UserRoleProviderExtension[DeleteError, FinanceGQLModel](),
            RbacProviderExtension[DeleteError, FinanceGQLModel](),
            LoadDataExtension[DeleteError, FinanceGQLModel]()
        ],
    )   
    async def finance_delete(
        self,
        info: strawberry.Info,
        finance: FinanceDeleteGQLModel
    ) -> typing.Optional[DeleteError[FinanceGQLModel]]:
        return await Delete[FinanceGQLModel].DoItSafeWay(info=info, entity=finance)
    
