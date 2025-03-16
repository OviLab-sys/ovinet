# Code Citations

## License: unknown
https://github.com/teammurphy/Related_Service_Scheduler_Backend/tree/cbcb86cf4b6b4ebf9cbe2f90d1ad580aad599c8f/app/authentication.py

```
], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, username: str, password: str):
    user
```


## License: unknown
https://github.com/msi89/fastapi-tortoise-mvc-api/tree/7dd7b39e4305d1ecac5a274485786ec66fd835bb/core/middlewares/auth.py

```
:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else
```


## License: unknown
https://github.com/Wereks/notif-api/tree/2d0340108afb2c527a52a71dc90cab733bb22897/app/auth.py

```
["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, username: str, password:
```


## License: unknown
https://github.com/lie-flat/cfps-jupyterhub/tree/ccbde788bf3ce72ce7b61efe2757ecbd16f70b64/backend/security.py

```
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password
```


## License: unknown
https://github.com/guyver2/battlechess/tree/5604051d66a64f11333567b8b45cf3e85056c690/server/crud.py

```
:
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=
```

