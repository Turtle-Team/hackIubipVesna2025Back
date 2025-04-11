from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import declarative_base

Base = declarative_base()
engine = create_engine('postgresql://hackiubip:iLWPdGXu5UngKTk58dGnwj3Brwpe4qE8@62.109.29.83/iubip2025', echo=True)
Session = sessionmaker(bind=engine)
