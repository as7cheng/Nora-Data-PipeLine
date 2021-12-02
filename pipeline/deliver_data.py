"""
File to deliver transformed data entries to the table in database
"""

import transform_data
import data_log
from database import SESS
from sqlalchemy import exc

# Prompt message for data log sent to Slack
START_PROMPT = '------Start DELIVERING data entris------'
END_PROMPT = '------Ended DELIVERING data entries, '

def insert(data_entry) -> int:
    """
    Helper function to insert data entry into table on RDS
    """
    try:
        SESS.add(data_entry)
        SESS.commit()
        print(f"Data entry {data_entry.id} has been inserted")
        data_log.send_log(f"(Done). {data_entry.id}")
        data_log.send_log(data_entry.timestamp)
        return 1
    except exc.SQLAlchemyError as error:
        print(error)
        data_log.send_log(f"(Failed). {data_entry.id}")
        data_log.send_log("Data entry is already in the DB")
        SESS.rollback()
    return 0

def deliver() -> str:
    """
    Helper function to deliver data to database on RDS
    """
    data_entries = transform_data.transform()
    data_log.send_log(START_PROMPT)
    count = 0
    for data_entry in data_entries:
        count += insert(data_entry)
    data_log.send_log(f"{END_PROMPT}{count} data entries delivered------")
    return f"{count} data inserted"
