# app/database/connection.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.config import settings
from sqlalchemy.ext.declarative import declarative_base
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


Base = declarative_base()


def get_database_url():
    return f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"


def create_db_engine(max_retries=5, retry_interval=5):
    retry_count = 0
    while retry_count < max_retries:
        try:
            engine = create_engine(
                get_database_url(),
                pool_pre_ping=True,  # This will test the connection before using it
            )
            # Test the connection
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
                connection.commit()  # Make sure to commit the transaction
            logger.info("Successfully connected to the database")
            return engine
        except Exception as e:
            retry_count += 1
            if retry_count == max_retries:
                logger.error(
                    f"Failed to connect to the database after {max_retries} attempts: {str(e)}"
                )
                raise e
            logger.warning(
                f"Database connection attempt {retry_count} failed. Retrying in {retry_interval} seconds..."
            )
            time.sleep(retry_interval)


engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
