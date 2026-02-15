"""db module."""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

_PROD_URL = os.environ["PROD_DB_URL"]
_STAGING_URL = os.environ["STAGING_DB_URL"]

engine = create_engine(_PROD_URL)
engine_staged = create_engine(_STAGING_URL)

__all__ = ["engine", "engine_staged"]
