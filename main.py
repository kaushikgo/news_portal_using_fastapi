from fastapi import FastAPI
from sample_news_portal.routes import user, news, category, tags
 



app = FastAPI()

app.include_router(user.user)
app.include_router(news.news)
app.include_router(category.category)
app.include_router(tags.tag)



@app.get("/")
def read_root():
    return["Welcome to Sample News Portal"]