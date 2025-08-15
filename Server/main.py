from fastapi import FastAPI
from database import engine,Base
import models
from Routes import UserRoute

app=FastAPI()


Base.metadata.create_all(bind=engine)





@app.get("/")
async def root():
    return {"message": "FastAPI Q&A app is running"}


app.include_router(UserRoute.router)