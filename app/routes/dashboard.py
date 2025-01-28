from fastapi import APIRouter,status
from app.core.dependancies import db_dependancy
from app.core.auth_dependacies import user_dependancy
from app.services.dashboard_services import get_dashboard_graph_data,get_aggregate_data


dashboard_router=APIRouter(prefix='/api/dashboard',tags=["Dashboard"])


@dashboard_router.get('/graphs',status_code=status.HTTP_200_OK)
async def get_graph_data(db:db_dependancy,user:user_dependancy):
    graph_data=get_dashboard_graph_data(db,user)
    return graph_data

@dashboard_router.get('/financialData',status_code=status.HTTP_200_OK)
async def get_financialData(db:db_dependancy,user:user_dependancy):
    financialData=get_aggregate_data(db,user)
    return financialData