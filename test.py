import jwt
from time import time, sleep
key="mijnkey"





def get_token(expiration_time=2):
    
    return jwt.encode({'user_id':5, 'exp':time()+expiration_time}, key, algorithm ="HS256"  )

token_test = get_token()
print(token_test)
print("doet dit wel iets")

token_decode = jwt.decode(token_test, key, algorithms="HS256")
print(token_decode)
sleep(5)
token_decode = jwt.decode(token_test, key, algorithms="HS256")
print(token_decode)
