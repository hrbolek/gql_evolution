from __future__ import annotations

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.DBDefinitions.Domain_Events.EventTypeModel import EventTypeModel


DEFAULT_EVENT_TYPES = (
    {
        'id': uuid.UUID('11111111-1111-1111-1111-111111111111'),
        'name': 'Událost',
        'name_en': 'Event',
    },
    {
        'id': uuid.UUID('22222222-2222-2222-2222-222222222222'),
        'name': 'Schůzka',
        'name_en': 'Meeting',
    },
)


async def init_database_data(session: AsyncSession) -> None:
    """Idempotent seed hook for application startup.

    Keep this function small and explicit. It is called once from
    DatabaseRuntime.start(), after metadata.create_all().
    """

    for item in DEFAULT_EVENT_TYPES:
        existing = await session.get(EventTypeModel, item['id'])
        if existing is None:
            session.add(EventTypeModel(**item))

    await session.commit()
