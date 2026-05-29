# # db.py
# from sqlalchemy import create_engine #type: ignore
# from sqlalchemy.orm import sessionmaker, declarative_base #type: ignore

# # Aiven MySQL Database URL

# import os
# from dotenv import load_dotenv #type: ignore

# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")
# # Create engine with SSL enabled
# engine = create_engine(
#     DATABASE_URL,
#     connect_args={
#         "ssl": {
#             "ssl_mode": "REQUIRED"
#         }
#     }
# )

# SessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine
# )

# Base = declarative_base()


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()



from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# from dotenv import load_dotenv
import os

# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")
# DATABASE_URL = "mysql+pymysql://root:0070100@localhost:3306/attendance"

DATABASE_URL = "mysql+pymysql://root:fhSOWzQUksYlVTqNuqrtqkPonGkRBdUg@ballast.proxy.rlwy.net:30690/railway"


# Check DATABASE_URL
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl": {
            "ssl_mode": "REQUIRED"
        }
    },
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()