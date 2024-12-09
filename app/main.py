from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import Config
from app.routes.auth import auth_router
from app.core.db import init_db

version="v1"

app=FastAPI(title="SpendTrail",description="AI based expense tracker",version=version)


app.include_router(auth_router)

origins=[
    "https://spendtrail-rg06k5wup-rohan1007rjp-gmailcoms-projects.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"], 
)


if __name__=="__main__":
    
    init_db()
    
    if Config.environment=="development":
        print("Runnning in development environment")
    else:
        print("Running in production environment")    
    
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0", 
        port=8000,       
        reload=True 
    )