from fastapi import APIRouter, HTTPException, status, Query
from sample_news_portal.models.models import NewsModel
import datetime
from sample_news_portal.database.database import *
from sample_news_portal.schema.schema import *
from pymongo.collection import ObjectId
from typing import Optional
import validators
from PIL import Image
from io import BytesIO

news = APIRouter()

@news.post("/news/create_news", tags= ["News"])
def add_news(newsinfo : NewsModel):
    news_image = newsinfo.Image
    if not validators.url(news_image):
        try:
            with Image.open(BytesIO(news_image.encode())):
                pass 
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail="Invalid newsImage. It must be a valid URL or image file."
            )
    newsinfo = dict(newsinfo)
    newsinfo.update(
        {"Created_at": datetime.datetime.now(), "Is_Published": False, "Publish_Date": None}
        )
    db.News.insert_one(newsinfo)
    return{"message": "news created"}

@news.put("/news/update_news", tags=["News"])
def update_news(News_id: str, newsinfo: NewsModel):
    newsinfo = db.News.find_one({"_id": ObjectId(News_id)})
    if newsinfo is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="News article not found"
            )
    updating_news ={}
        
    if "News_Title" in newsinfo:
        updating_news["News_Title"] = newsinfo["News_Title"]
    if "BriefDescription" is not None:
        updating_news["BriefDescription"] = newsinfo["BriefDescription"]
    if "Content" is not None:
        updating_news["Content"] = newsinfo["Content"]
    if "Image" is not None:
        updating_news["Image"] = newsinfo["Image"]
    if "Tags" is not None:
        updating_news["Tags"] = newsinfo["Tags"]
    if "Category" is not None:
        updating_news["Category"] = newsinfo["Category"]
    
    if not updating_news:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail=" No update operation provided"
        )
    
    db.News.update_one({"_id": ObjectId(News_id)},{"$set": updating_news})
    
    return{"message":"News article update successfully","updated_news": Newsupdatingschema(newsinfo)}

@news.put("/news/publish_news", tags=["News"])
def publish_news(News_id: str, Status: str):
    existing_news = db.News.find_one({"_id": ObjectId(News_id)})
    if existing_news is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="News article not found"
        )
    Status = Status.lower()
    update_data = {
        "$set": {
            "Status" : Status,
        }
    }
    
    if Status == "published":
        update_data["$set"]["Publish_Date"] = datetime.datetime.now()
        update_data["$set"]["Is_Published"] = True
        message = "News published successfully"
    elif Status == "draft":
        update_data["$set"]["Is_Published"] = False
        message = " News drafted successfully"
    elif Status =="archived":
        update_data["$set"]["Is_Published"] = False
        message = " News archived succesfully"
        
    update = db.News.update_one({"_id": ObjectId(News_id)}, update_data)
    if update.modified_count == 0:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="Failed to news article"
        )
    return{"message": message}

@news.put("/news/update_publishednews", tags=["News"])
def updating_publishednews(
    News_id: str, 
    title: str="=",
    brief_description: str="",
    content: str="",
    image: str="",
    tags: str="",
    category: str="",):
    
    existing_news = db.News.find_one({"_id": ObjectId(News_id)})
    if existing_news is None:
        raise HTTPException(
            status_code=404, detail="News article not found"
        )

    if existing_news["Status"].lower() != "published":
        raise HTTPException(
            status_code=400, detail="News article is not published"
        )

    update_data = {
        "$set": {
            "Status": "draft",
            "Is_Published": False,
            "News_Title": title,
            "BriefDescription": brief_description,
            "Content": content,
            "Image": image,
            "Tags": tags,
            "Category": category,
            "Updated_at": datetime.datetime.now(),
        }
    }
    
    update = db.News.update_one({"_id": ObjectId(News_id)}, update_data)
    
    if update.modified_count == 0:
        raise HTTPException(
            status_code=400, detail="Failed to update news article"
        )

    return {"message": "News article updated successfully to draft"}

@news.get("/news/get_all_news", tags=["News"])
def get_all_news():
    all_news = list(db.News.find({}))
    
    if not all_news:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail ="No News articles found"
        )
    for news_article in all_news:
        news_article["_id"] = str(news_article["_id"])
    return{"news_article": all_news}

@news.get("/news/filter_news", tags=["News"])
def filter_news(
    tags: Optional[str]= Query(None, description="Filter by tags"),
    category: Optional[str]= Query(None, description="Filter by category")
    
    ):
    news_query ={}
    if tags:
        news_query["Tags"]= tags
    if category: 
        news_query["Category"]= category
        
    filter_news = list(db.News.find(news_query))
    
    if not filter_news:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="no  news articles found matching the filter"
        
        )
    for news_article in filter_news:
        news_article["_id"] =str(news_article["_id"])  
        
    return{"filter_news": filter_news}  
        




