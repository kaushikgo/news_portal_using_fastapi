from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from approutes import admin, news, category, tags, reader
 



app = FastAPI()


origins =[
    
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.admin)
app.include_router(news.news)
app.include_router(category.category)
app.include_router(tags.tag)
app.include_router(reader.reader)



@app.get("/")
def read_root():
    return["Welcome to Sample News Portal"]