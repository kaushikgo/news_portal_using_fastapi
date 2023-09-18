from fastapi import APIRouter, HTTPException, status
from  models.models import AdminModel
import datetime
from passlib.context import CryptContext 
from schema.schema import *
from database.database import *
from pymongo.collection import ObjectId
import email.utils
import validators
from urllib.parse import quote



admin = APIRouter()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")

@admin.post("/admin/create", tags= ["Admin"])
def add_userinfo(userinfo : AdminModel):
    valid_role = ["user", "admin", "editor", "content"]
    if userinfo.Role.lower() not in valid_role:
        raise HTTPException(
            status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid Role. Allowed roles are only user, admin, editor,content"
        )
    
    user_image = str(userinfo.AdminImage)
    
    # if not validators.url(user_image):
    #     try:
    #         with Image.open(user_image.encode()):
    #             pass 
    #     except Exception as e:
    #         raise HTTPException(
    #             status_code=400,
    #             detail="Invalid UserImage. It must be a valid URL or image file."
    #         )
    
    
    
    if not validators.email(userinfo.Email):
        raise HTTPException(
            status.HTTP_406_NOT_ACCEPTABLE, datail="Invalid Email Address "
        )
    
    if db.Admin.find_one({"Email": userinfo.Email}) is not None:
        raise HTTPException(
            status.HTTP_406_NOT_ACCEPTABLE, detail = "Email Already Exists"
            )
    userinfo.Password = pwd_context.hash(
        userinfo.Password
        )
    userinfo = dict(userinfo)
    userinfo.update(
        {"Created_at": datetime.datetime.now(),"Is_Activated": True}
        )
    userinfo["UserImage"] = user_image
    db.Admin.insert_one(userinfo)
    
    return{
        "message": "successfully inserted"
        }
    

@admin.post("/admin/login", tags=["Admin"])
def login_userinfo(Email : str, Password: str):
    findindinfo = db.Admin.find_one({"Email": Email})
    if findindinfo is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail= "Email Not Found"
        ) 
    pwdmatch = pwd_context.verify(Password,findindinfo["Password"])
    if pwdmatch == False:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail= "Incorrect Password "
            )
    findindinfo = dict(findindinfo)
    findindinfo["_id"] = str(findindinfo["_id"])
    return["login successful", Adminschema(findindinfo)]

@admin.get("/admin/my_profile", tags=["Admin"])
def myprofile( ID:str ):
    userinfo = db.Admin.find_one({"_id" : ObjectId(ID) })
    if userinfo is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Not Found"
        )
    userinfo = dict(userinfo)
    userinfo["_id"] = str(userinfo["_id"])
    return{"userinfo": userinfo}
    
@admin.put("/admin/patch_profile", tags=["Admin"])
def updating_myprofile(ID : str, New_Bio:str, Is_Activated: bool):
    userinfo = db.Admin.find_one({"_id" : ObjectId(ID)})
    if userinfo is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Not Found"
        )
    filter_query = {"_id": ObjectId(ID)}
    updating ={}

    if New_Bio is not None:
        updating["Bio"] =  New_Bio

    if Is_Activated is not None:
        updating["Is_Activated"] = Is_Activated
    print(updating)
    if not updating:
        raise HTTPException(status_code=400, detail="No update operations provided")

    updatinguser = db.Admin.update_one(filter_query, {"$set":updating})
    
    updated_userinfo = db.Admin.find_one(filter_query)
    if updated_userinfo is None:
        raise HTTPException(status_code=404, detail="User not found after update")

    updated_userinfo["_id"] = str(updated_userinfo["_id"])
    return("message", updated_userinfo)
    