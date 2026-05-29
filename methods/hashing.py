# from passlib.context import CryptContext
# pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

# class Hash():
#     @staticmethod
#     def bcrypt(password: str): # type: ignore
#         return pwd_cxt.hash(password)

#     @staticmethod
#     def verify(hashed_password: str, plain_password: str): # type: ignore
#         return pwd_cxt.verify(plain_password, hashed_password) 
    
from passlib.context import CryptContext

pwd_cxt = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

class Hash:

    @staticmethod
    def bcrypt(password: str):
        return pwd_cxt.hash(password[:72])

    @staticmethod
    def verify(hashed_password, plain_password):
        return pwd_cxt.verify(
            plain_password[:72],
            hashed_password
        )