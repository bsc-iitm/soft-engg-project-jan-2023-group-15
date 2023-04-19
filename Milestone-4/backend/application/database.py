from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.ext.declarative import declarative_base

engine = None
#declarative_base() callable returns a new base class from which all mapped classes should inherit. When the class definition is completed, a new Table and mapper() will have been generated
# Base = declarative_base
db = SQLAlchemy()