from decouple import config

from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    BOOLEAN,
    DateTime,
    create_engine,
    Float,
    ForeignKey,
    sql,
)

from databases import Database

# db config
DATABASE_URI = config("DB_URI")


metadata = MetaData()

database = Database(DATABASE_URI)


ledger = Table(
    "accounts",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("balance", Float),
    Column("account_id", String(), unique=True),
    Column("active", BOOLEAN),
    Column("user", Integer, ForeignKey("users.id")),
    Column("created_at", DateTime(timezone=True), server_default=sql.func.now()),
    Column("updated_at", DateTime(timezone=True), onupdate=sql.func.now()),
)

users = Table(
    "users",
    metadata,
    Column("id", Integer(), primary_key=True),
    Column("firstName", String(), nullable=False),
    Column("lastName", String(), nullable=False),
    Column("email", String(), unique=True, nullable=False),
    Column("phone", String(), unique=True, nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=sql.func.now()),
    Column("updated_at", DateTime(timezone=True), onupdate=sql.func.now()),
)

engine = create_engine(DATABASE_URI, echo=True)


metadata.create_all(engine)
