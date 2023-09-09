import pymongo


app = pymongo.MongoClient("mongodb://charnendraddid:zyxwvuts987@ac-fdolg61-shard-00-00.eguhnjc.mongodb.net:27017,ac-fdolg61-shard-00-01.eguhnjc.mongodb.net:27017,ac-fdolg61-shard-00-02.eguhnjc.mongodb.net:27017/?replicaSet=atlas-k36b71-shard-0&ssl=true&authSource=admin")
db = app["NewsPortal"]
Admin = db["Userinfo"]
News = db["Newsinfo"]
Category = db["Categoryinfo"]
Tags = db["Taginfo"]