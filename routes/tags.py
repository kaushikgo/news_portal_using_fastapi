from fastapi import APIRouter, HTTPException, status
from sample_news_portal.models.models import TagsModel
import datetime
from sample_news_portal.database.database import *
from sample_news_portal.schema.schema import *
from pymongo.collection import ObjectId
from typing import Optional

tag = APIRouter()

@tag.post("/tags/add_tags", tags=["Tags"])
def add_tags(tagsinfo : TagsModel):
    news_list = list( db.News.find({"Tags":tagsinfo.Tag, "Is_Published": True}))
    news_count = len(news_list)
    newsIds=[]
    for n in news_list:
        newsIds.append(str(n["_id"]))
    tagsinfo = dict(tagsinfo)
    tagsinfo.update(
        {"Is_Active": True, "Created_at": datetime.datetime.now(),"News_IDs": newsIds, "News_Published": news_count}
    )
    db.Tags.insert_one(tagsinfo)
    return{"message": "successfully created tags"}

@tag.get("/tags/get_all_news", tags=["Tags"])
def read_tags():
    all_tags = list(Tags.find({}))
    
    if all_tags == []:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail= "No Tags articles foound"
        )
    for tag in all_tags:
        tag["_id"] = str(tag["_id"])
    return{"all_tags": all_tags}

@tag.delete("/tag/delete_tag/{tag_id}", tags=["Tags"])
def deletetagy(tag_id: str):
    # Check if the category_id is a valid ObjectId
    if not ObjectId.is_valid(tag_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid category ID"
        )

    # Check if the category exists
    tag = db.Tags.find_one({"_id": ObjectId(tag_id)})

    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    # Delete the category
    db.Tags.delete_one({"_id": ObjectId(tag_id)})

    return {"message": "tag deleted successfully"}