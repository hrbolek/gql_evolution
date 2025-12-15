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
class ProjectInputFilter:
    id: IDType


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



class ProjectInsertGQLModel(InputModelMixin):
    getLoader = ProjectGQLModel.getLoader

    id: typing.Optional[IDType] = strawberry.field(
        description="""Event id""",
        default=None
    )

    rbacobject_id: IDType = strawberry.field(
        description="""Definitoin of access control"""
    )

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
            UserAccessControlExtension[InsertError, ProjectGQLModel](
                roles=[
                    "plánovací administrátor", 
                    "administrátor"
                ]
            ),
            UserRoleProviderExtension[InsertError, ProjectGQLModel](),
            RbacInsertProviderExtension[InsertError, ProjectGQLModel](
                rbac_key_name="rbacobject_id"    
            ),
        ],
    )
    async def project_insert(
        self,
        info: strawberry.Info,
        project: ProjectInsertGQLModel,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Union[ProjectGQLModel, InsertError[ProjectGQLModel]]:
        return await Insert[ProjectGQLModel].DoItSafeWay(info=info, entity=project)
    


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
    async def project_update(
        self,
        info: strawberry.Info,
        project: ProjectUpdateGQLModel
    ) -> typing.Union[ProjectGQLModel, UpdateError[ProjectGQLModel]]:
        return await Update[ProjectGQLModel].DoItSafeWay(info=info, entity=project)
    


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
    async def project_delete(
        self,
        info: strawberry.Info,
        project: ProjectDeleteGQLModel
    ) -> typing.Optional[DeleteError[ProjectGQLModel]]:
        return await Delete[ProjectGQLModel].DoItSafeWay(info=info, entity=project)
    
