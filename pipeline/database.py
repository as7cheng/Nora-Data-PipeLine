"""
File to create connection of Database hold on RDS
"""

import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Get connection info from the security file
with open('/var/task/security.json', 'rb') as f:
    DATA = json.load(f)
    DB_URL = DATA['DB_URL']
    DB_PORT = DATA['DB_PORT']
    DB_NAME = DATA['DB_NAME']
    DB_USER = DATA['DB_USER']
    DB_PSW = DATA['DB_PSW']

RDS_URL = f"postgresql://{DB_USER}:{DB_PSW}@{DB_URL}:{DB_PORT}/{DB_NAME}"
ENGINE = create_engine(RDS_URL)
SESSION = sessionmaker(bind=ENGINE)

SESS = SESSION()
