from fastapi import HTTPException,APIRouter,Depends,UploadFile,File
from sqlalchemy.orm import Session
from models.Users import users
from Schema.UserSchema import UserBase,UpdateUserBase,UpdateUserPassword,LoginUserBase
from database import get_db
import bcrypt
from utils.Cloudinary_config import cloudinary
from cloudinary.uploader import upload
router=APIRouter(prefix='/users',tags=["Users"])


@router.post('/create_user')
async def create_user(user:UserBase,db: Session= Depends(get_db)):
    existing_user=db.query(users).filter(users.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password=bcrypt.hashpw(user.password.encode('utf-8'),bcrypt.gensalt())
    new_user=users(
        username=user.username,
        email=user.email,
        password=hashed_password.decode('utf-8'),
        address=user.address
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return {"message": "User created successfully", "user": new_user}


@router.put("/profile_pic/{user_id}")
async def Upload_Porfile_pic(user_id:str,file: UploadFile = File(...),db: Session= Depends(get_db)):
    try:
        user=db.query(users).filter(users.id==user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Upload file to Cloudinary
        result = upload(file.file, folder="Studymate/profile_pics")  # folder in Cloudinary
        image_url = result.get("secure_url")

        if not image_url:
            raise HTTPException(status_code=500, detail="Failed to upload image to Cloudinary")
        
        user.profile_pic_url = image_url
        db.commit()
        db.refresh(user)

        return {"message": "Profile picture uploaded successfully", "profile_pic": image_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    

@router.put('/update/{user_id}')
async def update_user(user_id:str, user:UpdateUserBase, db: Session= Depends(get_db)):
    existing_user = db.query(users).filter(users.id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_user.username = user.username
    existing_user.address = user.address

    db.commit()
    db.refresh(existing_user)

    return {"message": "User updated successfully", "user": existing_user}

@router.put('/update_password/{user_id}')
async def update_user_password(user_id:str, password: UpdateUserPassword , db: Session= Depends(get_db)):
    existing_user = db.query(users).filter(users.id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not bcrypt.checkpw(password.old_password.encode('utf-8'), existing_user.password.encode('utf-8')):   
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    hashed_password = bcrypt.hashpw(password.new_password.encode('utf-8'), bcrypt.gensalt())
    existing_user.password = hashed_password.decode('utf-8')

    db.commit()
    db.refresh(existing_user)

    return {"message": "User password updated successfully", "user": existing_user}

@router.post('/login')
async def login_user(user:LoginUserBase, db: Session= Depends(get_db)):
    existing_user= db.query(users).filter(users.email==user.credential).first()
    if not existing_user:
        existing_user = db.query(users).filter(users.username==user.credential).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt.checkpw(user.password.encode('utf-8'), existing_user.password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Invalid password.")

    return {"message": "Login successful", "user": existing_user}       