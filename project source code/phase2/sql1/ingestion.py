# from sqlalchemy import Column, Integer, String, Float,DateTime,create_engine
# from pydantic import BaseModel
# from sqlalchemy.orm import sessionmaker,declarative_base
# import pandas as pd
# from datetime import datetime
# from staging import session


# class IngestionLog(BaseModel): 

#     __tablename__ = "ingestion_log" 

 

#     log_id = Column(Integer, primary_key=True, autoincrement=True) 

#     table_name = Column(String(100)) 

#     load_time = Column(DateTime) 

#     row_count = Column(Integer) 

#     status = Column(String(20)) 

 

 

# log = IngestionLog( 

#     table_name="staging_customer", 

#     load_time=datetime.now(), 

#     row_count=len(df), 

#     status="SUCCESS" 

# ) 

 

# session.add(log) 

# session.commit() 