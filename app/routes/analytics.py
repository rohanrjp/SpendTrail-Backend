from app.core.auth_dependacies import user_dependancy
from app.core.dependancies import db_dependancy
from fastapi import APIRouter,status
from app.services.analytics_services import get_monthlyData,get_savingsData,get_expenseGrowthData,get_overviewData


analytics_router=APIRouter(prefix='/api/analytics',tags=["Analytics"])

@analytics_router.get('/graph_data',status_code=status.HTTP_200_OK)
async def get_graph_data(db:db_dependancy,user:user_dependancy):
    
    monthlyData=get_monthlyData(db,user)
    savingsData=get_savingsData(db,user)
    expenseGrowthData=get_expenseGrowthData(db,user)
    overviewData=get_overviewData(db,user)
    
    overall_analytics_data={
        "monthlyData":monthlyData,
        "savingsData":savingsData,
        "expenseGrowthData":expenseGrowthData,
        "overviewData":overviewData
    }
    
    return overall_analytics_data
    
    
    