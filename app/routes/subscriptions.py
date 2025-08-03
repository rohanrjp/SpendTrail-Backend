from fastapi import APIRouter, status  
from app.core.dependancies import db_dependancy  
from app.core.auth_dependacies import user_dependancy  
from app.schemas.subscription_schemas import subscription, updated_subscription  
from app.services.subscription_services import create_new_subscription, get_all_subscription, update_subscription
  
subscription_router = APIRouter(prefix="/api", tags=["Subscriptions"])  

@subscription_router.get("/subscriptions", status_code= status.HTTP_200_OK)
async def get_all_subscriptions(db: db_dependancy, user: user_dependancy):
    all_subscriptions = get_all_subscription(user, db)
    return all_subscriptions

  
@subscription_router.post("/create_subscription", status_code=status.HTTP_201_CREATED)  
async def new_subscription(db: db_dependancy, input_subscription: subscription, user: user_dependancy):  
    create_new_subscription(user, db, input_subscription)  
    return {"message": "Subscription created"}

@subscription_router.put("/update_subscription",status_code=status.HTTP_200_OK)
async def udpdate_subscription_route(db: db_dependancy, user: user_dependancy, input_subscription:updated_subscription):
    after_update_subscription = update_subscription(db, user, input_subscription)
    return after_update_subscription
     