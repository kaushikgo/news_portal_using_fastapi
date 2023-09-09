from pydantic import BaseModel, HttpUrl, EmailStr


class User(BaseModel):
    First_Name : str
    Last_Name : str
    UserImage : HttpUrl
    Email : EmailStr
    Password : str 
    Bio: str
    Role : str = "User"

class NewsModel(BaseModel):
    News_Title : str
    BriefDescription: str
    Content : str
    Author : str
    Image: HttpUrl
    Tags : str
    Category : str
    Language : str
    Status : str ="Draft"
    Viewcount : int = 0
    Related_News : str

class CategoryModel(BaseModel):
    Category : str
    Related_Tags : str

class TagsModel(BaseModel):
    Tag : str
    Released_Category : str

