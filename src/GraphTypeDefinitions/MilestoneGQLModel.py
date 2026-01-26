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
class MilestoneInputFilter:
    id: IDType


@strawberry.federation.type(
    description="""Entity representing a Milestone""",
    keys=["id"]
)

class MilestoneGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).MilestoneModel

    name: typing.Optional[str] = strawberry.field(
        description="Name of the milestone",
        default=None
    )

    description: typing.Optional[str] = strawberry.field(
        description="Description of the milestone",
        default=None
    )

    duedate: typing.Optional[datetime.datetime] = strawberry.field(
        description="Due date of the milestone",
        default=None
    )

    iscompleted: bool = strawberry.field(
        description="Is the milestone completed?",
        default=False
    )

    project_id: typing.Optional[IDType] = strawberry.field(
        description="Reference to the project",
        default=None
    )

@strawberry.interface(
    description="""Milestone queries"""
)
class MilestoneQuery:
    milestone_by_id: typing.Optional[MilestoneGQLModel] = strawberry.field(
        description="""get a milestone by its id""",
        permission_classes=[OnlyForAuthentized],
        resolver=MilestoneGQLModel.load_with_loader
    )

    milestone_page: typing.List[MilestoneGQLModel] = strawberry.field(
        description="""get a page of milestones""",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[MilestoneGQLModel](whereType=MilestoneInputFilter)
    )

from uoishelpers.resolvers import TreeInputStructureMixin, InputModelMixin
@strawberry.input(
    description="""Input type for creating a Milestone"""
)
class MilestoneInsertGQLModel(InputModelMixin):
    getLoader = MilestoneGQLModel.getLoader

    id: typing.Optional[IDType] = strawberry.field(
        description="""Milestone id""",
        default=None
    )
    name: typing.Optional[str] = strawberry.field(
        description="Name of the milestone",
        default=None
    )
    description: typing.Optional[str] = strawberry.field(
        description="Description of the milestone",
        default=None
    )
    duedate: typing.Optional[datetime.datetime] = strawberry.field(
        description="Due date of the milestone",
        default=None
    )
    iscompleted: bool = strawberry.field(
        description="Is the milestone completed?",
        default=False
    )
    rbacobject_id: IDType = strawberry.field(
        description="""Definitoin of access control"""
    )
    createdby_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="""Input type for updating a Milestone"""
)
class MilestoneUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""Milestone id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="timestamp"
    )
    name: typing.Optional[str] = strawberry.field(
        description="Name of the milestone",
        default=None
    )
    description: typing.Optional[str] = strawberry.field(
        description="Description of the milestone",
        default=None
    )
    duedate: typing.Optional[datetime.datetime] = strawberry.field(
        description="Due date of the milestone",
        default=None
    )
    iscompleted: typing.Optional[bool] = strawberry.field(
        description="Is the milestone completed?",
        default=None
    )
    changedby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="""Input type for deleting a Milestone"""
)
class MilestoneDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""Milestone id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""last change""",
    )

@strawberry.interface(
    description="""Milestone mutations"""
)
class MilestoneMutation:
    @strawberry.mutation(
        description="""Insert a Milestone""",
        permission_classes=[
            OnlyForAuthentized
            # SimpleInsertPermission[MilestoneGQLModel](roles=["administrátor"])
        ],
        extensions=[
            # UpdatePermissionCheckRoleFieldExtension[GroupGQLModel](roles=["administrátor", "personalista"]),
            UserAccessControlExtension[InsertError, MilestoneGQLModel](
                roles=[
                    "plánovací administrátor", 
                    "administrátor"
                ]
            ),
            UserRoleProviderExtension[InsertError, MilestoneGQLModel](),
            RbacInsertProviderExtension[InsertError, MilestoneGQLModel](
                rbac_key_name="rbacobject_id"    
            ),
        ],
    )
    async def milestone_insert(
        self,
        info: strawberry.Info,
        milestone: MilestoneInsertGQLModel,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Union[MilestoneGQLModel, InsertError[MilestoneGQLModel]]:
        return await Insert[MilestoneGQLModel].DoItSafeWay(info=info, entity=milestone)
    


    @strawberry.mutation(
        description="""Update a Milestone""",
        permission_classes=[
            OnlyForAuthentized
            # SimpleUpdatePermission[MilestoneGQLModel](roles=["administrátor"])
        ],
        extensions=[
            # UpdatePermissionCheckRoleFieldExtension[GroupGQLModel](roles=["administrátor", "personalista"]),
            UserAccessControlExtension[UpdateError, MilestoneGQLModel](
                roles=[
                    "plánovací administrátor", 
                    # "personalista"
                ]
            ),
            UserRoleProviderExtension[UpdateError, MilestoneGQLModel](),
            RbacProviderExtension[UpdateError, MilestoneGQLModel](),
            LoadDataExtension[UpdateError, MilestoneGQLModel]()
        ],
    )
    async def milestone_update(
        self,
        info: strawberry.Info,
        milestone: MilestoneUpdateGQLModel
    ) -> typing.Union[MilestoneGQLModel, UpdateError[MilestoneGQLModel]]:
        return await Update[MilestoneGQLModel].DoItSafeWay(info=info, entity=milestone)
    


    @strawberry.mutation(
        description="""Delete a Milestone""",
        permission_classes=[
            OnlyForAuthentized,
            # SimpleDeletePermission[MilestoneGQLModel](roles=["administrátor"])
        ],
        extensions=[
            # UpdatePermissionCheckRoleFieldExtension[GroupGQLModel](roles=["administrátor", "personalista"]),
            UserAccessControlExtension[DeleteError, MilestoneGQLModel](
                roles=[
                    "plánovací administrátor", 
                    # "personalista"
                ]
            ),
            UserRoleProviderExtension[DeleteError, MilestoneGQLModel](),
            RbacProviderExtension[DeleteError, MilestoneGQLModel](),
            LoadDataExtension[DeleteError, MilestoneGQLModel]()
        ],
    )   
    async def milestone_delete(
        self,
        info: strawberry.Info,
        milestone: MilestoneDeleteGQLModel
    ) -> typing.Optional[DeleteError[MilestoneGQLModel]]:
        return await Delete[MilestoneGQLModel].DoItSafeWay(info=info, entity=milestone)
    
