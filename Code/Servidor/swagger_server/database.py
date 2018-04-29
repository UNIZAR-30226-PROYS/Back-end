from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from swagger_server.config import BaseConfig

engine = create_engine(BaseConfig.SQLALCHEMY_DATABASE_URI, convert_unicode=True)
