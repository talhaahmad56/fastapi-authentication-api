from fastapi import FastAPI , Depends , status , HTTPException 
from database import engine , get_db
from sqlalchemy.orm import Session
import models 
from schemas import UserResponse , UserCreate , UserUpdate
from models import User 
import auth
from fastapi.security import OAuth2PasswordRequestForm

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/register" , status_code=status.HTTP_201_CREATED , response_model= UserResponse)
def register(user : UserCreate ,db : Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=409 , detail="User already exists")

    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=409 , detail= "Email already exists")

    new_user = User(
        username = user.username,
        email = user.email,
        hashed_password = auth.hash_password(
            user.password
        )
        
    ) 

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/login", status_code=status.HTTP_200_OK)
def login(form_data : OAuth2PasswordRequestForm = Depends() , db:Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=401 , detail="Incorrect Password or Username")
    correct_password = auth.verify_password(
        form_data.password,
        user.hashed_password
    )
    if not correct_password:
        raise HTTPException(status_code=401 , detail="Incorrect Password or Username")

    access_token = auth.create_token({
        "sub" : str(user.id)
    })
    return {
        "access_token" : access_token,
        "token_type" : "bearer"
    }

@app.get("/me" , response_model=UserResponse)
def current_user(user = Depends(auth.get_current_user)):
    return user

@app.patch("/update" , response_model=UserResponse)
def update_user(data : UserUpdate , db : Session = Depends(get_db) , current_user : User = Depends(auth.get_current_user)):

    updates = data.model_dump(exclude_unset=True)

    if not updates:
        raise HTTPException(status_code=400 , detail="No field updated")
    
    if "username" in updates:
        taken = db.query(User).filter(User.username == updates["username"] , User.id != current_user.id).first()

        if taken:
            raise HTTPException(status_code=409 , detail="Username already exist")

    if "email" in updates:
        taken = db.query(User).filter(User.email == updates["email"] , User.id != current_user.id).first()

        if taken:
            raise HTTPException(status_code=409 , detail="Email already exist")
                
    if "password" in updates:
        current_user.hashed_password == auth.hash_password(updates.pop("password"))
        
    for field, value in updates.items():
        setattr(current_user, field, value) 
    db.commit()
    db.refresh(current_user)
    return current_user           

@app.delete("/delete" , status_code=status.HTTP_204_NO_CONTENT)
def delete_user(db : Session = Depends(get_db) , current_user : User = Depends(auth.get_current_user)):
    db.delete(current_user)
    db.commit()

    


    
