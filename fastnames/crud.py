"""CRUD operations and ORM services."""
from fastnames.database import async_session
from fastnames.models import Female, Male
from fastnames.schemas import Nickname
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError


async def get_nicknames(
    model: Male | Female,
    limit: int,
    startswith: str | None = None,
) -> list[Nickname]:
    """Read nicknames from DB."""
    async with async_session() as session:
        async with session.begin():
            if startswith:
                result = await session.execute(
                    select(model)
                    .where(model.name.startswith(startswith))
                    .limit(limit),
                )
            else:
                result = await session.execute(select(model).limit(limit))
            return result.scalars().all()


async def create_nicknames(
    model: Male | Female,
    names: list[str],
) -> list[Nickname]:
    """
    Add nicknames to DB.

    Exceptions:
        IntegrityError: If entry already exists in database
    """
    async with async_session() as session:
        async with session.begin():
            instances = []
            for name in names:
                instance = model(name=name)
                session.add(instance)
                instances.append(instance)
            try:
                await session.commit()
                return instances
            except IntegrityError:
                await session.rollback()
                return ['Nickname already exists!']
