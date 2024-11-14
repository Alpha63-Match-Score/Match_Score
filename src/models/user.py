from sqlalchemy import Column, String
from src.models.base import Base, BaseMixin


class User(Base, BaseMixin):
    """
    Database model representing "user" table in the database.
    UUID and table name are inherited from BaseMixin.
    """

    username = Column(String)
    password = Column(String)
