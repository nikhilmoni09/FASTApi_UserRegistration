from fastapi import Depends, FastAPI, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

IMGDIR = 'assets/'

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#create user
@app.post('/users/', response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    resp = crud.create_user(db=db, user=user)
    return resp


#get all users
@app.get('/users/', response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


#get user by user id
@app.get('/users/{user_id}', response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user


#User registration with profile picture
@app.post('/register_with_profile_pic')
async def register_with_profile_pic(
            file: UploadFile = File(...),
            email : str = Form(),
            password : str = Form(),
            phone : str = Form(),
            full_name : str = Form(),
            db: Session = Depends(get_db)):

    try:
        user = {}
        user['email'] = email
        user['password'] = password
        user['phone'] = phone
        user['full_name'] = full_name
        #Check email already exist
        db_email_user = crud.get_user_by_email(db, email=email)
        if db_email_user:
             return {
                 'Message': 'Email already registered',
                 'status': False }
        #Check phone already exist
        db_phone_user = crud.get_user_by_phone(db, phone=phone)
        if db_phone_user:
             return {
                 'Message': 'Phone already registered',
                 'status': False }
        resp = crud.register_user(db=db, user=user)
        #Upload profile pic
        content = await file.read()
        with open(f'{IMGDIR}{file.filename}', 'wb') as f:
            f.write(content)
        user['id'] = resp.id
        crud.upload_profile(db=db, user=user, profile_pic=file.filename)
        return {
                'Message': 'User created successfully',
                'data': resp.id,
                'status': True
                }
    except Exception as error:
        return {
                'Message': str(error),
                'status': False
                }


#Upload image
# @app.post('/upload_profile_pic')
# async def upload_profile_pic(file: UploadFile = File(...)):
#     content = await file.read()
#     with open(f'{IMGDIR}{file.filename}', 'wb') as f:
#         f.write(content)
#     return {'File': file.filename}
