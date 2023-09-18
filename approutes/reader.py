from fastapi import APIRouter, HTTPException, status
from  models.models import AdminModel
import datetime 
from schema.schema import *
from database.database import *
from pymongo.collection import ObjectId
import email.utils
import validators
from urllib.parse import quote

reader = APIRouter()


@reader.get("/reader/get_one_news", tags=["Reader"])
def read_news(News_id : str):
    
    finding = db.News.find_one({"_id": ObjectId(News_id) })
    if not finding:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail= "News article not found"
        )
    
    finding = dict(finding)
    finding["_id"] = str(finding["_id"])
    update_news = {
        "$inc" :{"Viewcount":1 }
        
    }
    db.News.update_one({"_id": ObjectId(News_id)},update_news)
    return{"finding":Readernewschema}