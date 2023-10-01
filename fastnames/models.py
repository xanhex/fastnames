"""SQLAchemy models."""
from fastnames.database import Base
from sqlalchemy import Column, Integer, String


class Male(Base):
    """Model for the male nickname."""

    __tablename__ = 'male'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    def __repr__(self) -> str:
        """To representation."""
        return self.name


class Female(Base):
    """Model for the female nickname."""

    __tablename__ = 'female'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    def __repr__(self) -> str:
        """To representation."""
        return self.name
