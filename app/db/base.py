#/home/sandeep/Projects/ScholarChat /app/db/base.py
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass


# IMPORTANT: force model registration
from app.models import *  # noqa