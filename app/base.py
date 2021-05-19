from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app import app
from elasticsearch import Elasticsearch

engine = create_engine('mysql+pymysql://root:insert_password@127.0.0.1:3306/hashoff')
Session = sessionmaker(bind=engine)
es = Elasticsearch([{"host":'localhost',"port":'9200'}])
Base = declarative_base()
