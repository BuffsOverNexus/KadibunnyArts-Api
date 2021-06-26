from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
postgres_engine = create_engine("postgresql+psycopg2://iowuiihzvshtuf:4cc7bbb48d3d1b806f96439e77bae92f0e73115906644fcbaa8a9fef6117729a@ec2-52-4-111-46.compute-1.amazonaws.com:5432/d73emt21v0ggo7", echo=True)
Session = sessionmaker(bind=postgres_engine)