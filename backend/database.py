"""
Database configuration and session management.

This module defines the SQLAlchemy engine, session factory and declarative
base used by the Farkle backend.  By centralising these definitions you can
easily point the application at different databases by changing the
``DATABASE_URL`` environment variable.  A helper function ``get_db`` is
provided to yield a database session in FastAPI endpoints.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# Determine the database connection URL.  Default to a local SQLite file.  To
# switch to PostgreSQL simply set DATABASE_URL to something like
# ``postgresql://user:password@host:port/database``.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./farkle.db")

# The ``connect_args`` are only required for SQLite.  They are ignored by
# PostgreSQL.  Setting ``check_same_thread=False`` allows SQLAlchemy to use
# threads in a development environment.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

# Configure the session factory.  We disable autocommit and autoflush so that
# changes are only persisted when we explicitly commit.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base class for our ORM models.
Base = declarative_base()


def get_db():
    """Yield a database session for FastAPI dependencies.

    The session is committed and closed automatically when the request
    finishes.  Use this dependency in path operations to access the
    database.  Example::

        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
