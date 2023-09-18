from pydantic import BaseModel, HttpUrl, EmailStr


class AdminModel(BaseModel):
    First_Name : str
    Last_Name : str
    AdminImage : HttpUrl
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
    Status : str ="draft"
    Viewcount : int = 0
    Related_News : str

class CategoryModel(BaseModel):
    Category : str
    Related_Tags : str

class TagsModel(BaseModel):
    Tag : str
    Related_Category : str

