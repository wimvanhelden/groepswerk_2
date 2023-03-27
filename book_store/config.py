class Config:
    #app config    
    SECRET_KEY = '22a742a01ab7bab950c22668922661b5'  #put this in seperate file  or config variable later....
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    #config for email ("forgot password" email)  
    #(not yet working... can't find mail server that works)
    """
    MAIL_SERVER = 'smtp.gmx.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = True
    MAIL_USERAME = "groepswerktwee@gmx.com"   #put this in seperate file later....
    MAIL_PASSWORD  = "1FlesHavana"  #put this in seperate file later....
    """

    #SQL database config: to be added later... store in seperate file....