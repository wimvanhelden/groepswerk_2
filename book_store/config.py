from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from config_data import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME


class Config:
    #app config    
      #put this in seperate file  or config variable later....
    database_connection = create_engine('mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(
        DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
        ))
    #database_connection = create_engine('mysql+mysqldb://root:MySQLWim33@127.0.0.1:3306/groepswerk_twee_bart_wim')
    # create conneciton to database
    SECRET_KEY = '22a742a01ab7bab950c22668922661b5'
    database_connection.connect()
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(
        DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
        )
 
# create a session by linking the engine
    Session = sessionmaker(bind = database_connection)
    session = Session()


