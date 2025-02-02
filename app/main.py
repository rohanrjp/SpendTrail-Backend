from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import Config
from app.routes.auth import auth_router
from app.core.db import init_db
from app.routes.functionality import functionality_router
from app.routes.ai import ai_router
from app.models.db_health_check import DBHealthCheck
from app.core.dependancies import db_dependancy
from app.core.utils import get_ist_datetime
from app.routes.dashboard import dashboard_router
from app.routes.analytics import analytics_router

version="v1"

app=FastAPI(title="SpendTrail",description="AI based expense tracker",version=version)


app.include_router(auth_router)
app.include_router(functionality_router)
app.include_router(ai_router)
app.include_router(dashboard_router)
app.include_router(analytics_router)

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

@app.get("/ping", tags=["Health Check"])
def ping(db:db_dependancy):
    current_time=get_ist_datetime()
    last_health_check=db.query(DBHealthCheck).order_by(DBHealthCheck.last_checked_time.desc()).first()
    if last_health_check:
        last_health_check.last_checked_time=current_time
        db.add(last_health_check)
    else:
        new_health_check=DBHealthCheck(last_checked_time=current_time)
        db.add(new_health_check)
    
    db.commit()  
          
    return {
        "message": "Service is running",
    }


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