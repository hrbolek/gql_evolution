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

EventInvitationGQLModel = typing.Annotated["EventInvitationGQLModel", strawberry.lazy(".EventInvitationGQLModel")]
EventInvitationInputFilter = typing.Annotated["EventInvitationInputFilter", strawberry.lazy(".EventInvitationGQLModel")]


@createInputs2
class ProjectInputFilter:
    id: IDType
    valid: bool


@strawberry.federation.type(
    description="""Entity representing a Project""",
    keys=["id"]
)
class ProjectGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).ProjectModel

    path: typing.Optional[str] = strawberry.field(
        description="""Materialized path representing the group's hierarchical location.  
Materializovaná cesta reprezentující umístění skupiny v hierarchii.""",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )


    vector: typing.Optional[typing.List[float]] = strawberry.field(
        name="vector",
        default=lambda: [0.0] * 1024,
        description="semantic vector, default is 1024 zeros",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    valid: typing.Optional[bool] = strawberry.field(
        name="valid_raw",
        description="""If it intersects current date""",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )

    @strawberry.field(
        name="valid",
        description="""Event duration, implicitly in minutes""",
        permission_classes=[
            OnlyForAuthentized,
            # OnlyForAdmins
        ],
    )
    def valid_(self) -> typing.Optional[bool]:
        if self.valid is not None:
            return self.valid
        now = datetime.datetime.now()
        if self.startdate and self.enddate:
            return self.startdate <= now <= self.enddate
        elif self.startdate:
            return self.startdate <= now
        elif self.enddate:
            return now <= self.enddate
        return False

@strawberry.interface(
    description="""Project queries"""
)
class ProjectQuery:
    project_by_id: typing.Optional[ProjectGQLModel] = strawberry.field(
        description="""get a project by its id""",
        permission_classes=[OnlyForAuthentized],
        resolver=ProjectGQLModel.load_with_loader
    )

    project_page: typing.List[ProjectGQLModel] = strawberry.field(
        description="""get a page of projects""",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[ProjectGQLModel](whereType=ProjectInputFilter)
    )

from uoishelpers.resolvers import TreeInputStructureMixin, InputModelMixin
@strawberry.input(
    description="""Input type for creating a Project"""
)



class ProjectInsertGQLModel(TreeInputStructureMixin):
    getLoader = ProjectGQLModel.getLoader

    id: typing.Optional[IDType] = strawberry.field(
        description="""Event id""",
        default=None
    )

    rbacobject_id: strawberry.Private[IDType] = None
    createdby_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="""Input type for updating a Project"""
)
class ProjectUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""Event id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="timestamp"
    )
    # parent_id: typing.Optional[IDType] = strawberry.field(
    #     description="""Event parent id""",
    #     default=None
    # )
    changedby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="""Input type for deleting a Project"""
)
class ProjectDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""Project id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""last change""",
    )

@strawberry.interface(
    description="""Project mutations"""
)
class ProjectMutation:
    @strawberry.mutation(
        description="""Insert a Project""",
        permission_classes=[
            OnlyForAuthentized
            # SimpleInsertPermission[ProjectGQLModel](roles=["administrátor"])
        ],
        extensions=[
            # UpdatePermissionCheckRoleFieldExtension[GroupGQLModel](roles=["administrátor", "personalista"]),
            UserAccessControlExtension[UpdateError, ProjectGQLModel](
                roles=[
                    "plánovací administrátor", 
                    # "personalista"
                ]
            ),
            UserRoleProviderExtension[UpdateError, ProjectGQLModel](),
            RbacProviderExtension[UpdateError, ProjectGQLModel](),
            LoadDataExtension[UpdateError, ProjectGQLModel](
                getLoader=ProjectGQLModel.getLoader,
                primary_key_name="masterevent_id"
            )
        ],
    )
    async def event_insert(
        self,
        info: strawberry.Info,
        event: ProjectInsertGQLModel,
        db_row: typing.Any,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Union[ProjectGQLModel, InsertError[ProjectGQLModel]]:
        return await Insert[ProjectGQLModel].DoItSafeWay(info=info, entity=event)
    


    @strawberry.mutation(
        description="""Update a Project""",
        permission_classes=[
            OnlyForAuthentized
            # SimpleUpdatePermission[ProjectGQLModel](roles=["administrátor"])
        ],
        extensions=[
            # UpdatePermissionCheckRoleFieldExtension[GroupGQLModel](roles=["administrátor", "personalista"]),
            UserAccessControlExtension[UpdateError, ProjectGQLModel](
                roles=[
                    "plánovací administrátor", 
                    # "personalista"
                ]
            ),
            UserRoleProviderExtension[UpdateError, ProjectGQLModel](),
            RbacProviderExtension[UpdateError, ProjectGQLModel](),
            LoadDataExtension[UpdateError, ProjectGQLModel]()
        ],
    )
    async def event_update(
        self,
        info: strawberry.Info,
        event: ProjectUpdateGQLModel
    ) -> typing.Union[ProjectGQLModel, UpdateError[ProjectGQLModel]]:
        return await Update[ProjectGQLModel].DoItSafeWay(info=info, entity=event)
    


    @strawberry.mutation(
        description="""Delete a Project""",
        permission_classes=[
            OnlyForAuthentized,
            # SimpleDeletePermission[ProjectGQLModel](roles=["administrátor"])
        ],
        extensions=[
            # UpdatePermissionCheckRoleFieldExtension[GroupGQLModel](roles=["administrátor", "personalista"]),
            UserAccessControlExtension[DeleteError, ProjectGQLModel](
                roles=[
                    "plánovací administrátor", 
                    # "personalista"
                ]
            ),
            UserRoleProviderExtension[DeleteError, ProjectGQLModel](),
            RbacProviderExtension[DeleteError, ProjectGQLModel](),
            LoadDataExtension[DeleteError, ProjectGQLModel]()
        ],
    )   
    async def event_delete(
        self,
        info: strawberry.Info,
        event: ProjectDeleteGQLModel
    ) -> typing.Optional[DeleteError[ProjectGQLModel]]:
        return await Delete[ProjectGQLModel].DoItSafeWay(info=info, entity=event)
    
