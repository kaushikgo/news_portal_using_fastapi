from fastapi import APIRouter, HTTPException, status
from models.models import CategoryModel
import datetime
from database.database import *
from schema.schema import *
from pymongo.collection import ObjectId
from typing import Optional

category = APIRouter()

@category.post("/category/add_category", tags=["category"])
def add_category(categoryinfo: CategoryModel):
    news_list = list(db.News.find({"Category":categoryinfo.Category, "Is_Published": True}))
    news_count = len(news_list)
    newsIds=[]
    for n in news_list:
        newsIds.append(str(n["_id"]))
    categoryinfo = dict(categoryinfo)
    categoryinfo.update(
        {"Is_Active": True, "Created_at": datetime.datetime.now(),  "News_IDs": newsIds, "News_Published": news_count}
    )
    db.Category.insert_one(categoryinfo)
    return{"message":"category created"}

@category.get("/category/get_all_news", tags=["category"])
def read_category():
    all_category = list(Category.find({}))
    
    if all_category == []:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail= "No Category articles found"
        )
    for category in all_category:
        category["_id"] = str(category["_id"])
    return{"all_category": all_category}

@category.delete("/category/delete_category/{category_id}", tags=["category"])
def delete_category(category_id: str):

    if not ObjectId.is_valid(category_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid category ID"
        )

    category = db.Category.find_one({"_id": ObjectId(category_id)})

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    db.Category.delete_one({"_id": ObjectId(category_id)})

    return {"message": "Category deleted successfully"}


