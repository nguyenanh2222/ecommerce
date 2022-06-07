from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

host = "localhost"
port = "5432"
database = "postgres"
username = "postgres"
password = "example"

engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}',
                       connect_args={'options': '-csearch_path={}'.format("ecommerce")})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = sessionmaker(bind=engine, future=True)
