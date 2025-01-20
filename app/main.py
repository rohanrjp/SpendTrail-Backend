from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import Config
from app.routes.auth import auth_router
from app.core.db import init_db
from app.routes.functionality import functionality_router
from app.routes.ai import ai_router

version="v1"

app=FastAPI(title="SpendTrail",description="AI based expense tracker",version=version)


app.include_router(auth_router)
app.include_router(functionality_router)
app.include_router(ai_router)

origins=[
    "*"
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