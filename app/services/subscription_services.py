import calendar
from app.models.subscriptions import Subscriptions  
from app.models.budgets import Budgets  
from app.models.expenses import Expenses
from app.models.subscriptions import Subscriptions, FrequencyType
from app.schemas.subscription_schemas import subscription,updated_subscription
from app.schemas.functionality_schemas import budget, expense
from app.services.functionality_services import create_new_expense, create_new_budget
from sqlalchemy.orm import Session  
from app.core.utils import get_ist_datetime  
from fastapi import HTTPException, status  
from sqlalchemy import extract  
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta


def get_all_subscription(user, db: Session):
    return db.query(Subscriptions).filter(
        Subscriptions.owner == user.id,
    ).all()
  
def create_new_subscription(user, db: Session, input_subscription: subscription):   
    current_month = get_ist_datetime().month  
    current_year = get_ist_datetime().year  
      
    corresponding_budget = db.query(Budgets).filter(  
        Budgets.budget_category == input_subscription.category,  
        Budgets.owner == user.id,  
        extract('month', Budgets.budget_created_date) == current_month,  
        extract('year', Budgets.budget_created_date) == current_year  
    ).first()  
  
    if not corresponding_budget:  
        raise HTTPException(  
            status_code=status.HTTP_400_BAD_REQUEST,  
            detail=f"No corresponding budget exists for category '{input_subscription.category}'"  
        )  
  
    try:  
        new_subscription = Subscriptions(  
            name=input_subscription.name,  
            amount=input_subscription.amount,  
            category=input_subscription.category,  
            frequency=input_subscription.frequency,  
            start_date=input_subscription.start_date,  
            end_date=input_subscription.end_date,  
            repeat_count=input_subscription.repeat_count,  
            owner=user.id  
        )  
        db.add(new_subscription)  
        db.commit()  
        db.refresh(new_subscription)  
  
    except Exception as e:  
        db.rollback()  
        raise HTTPException(  
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  
            detail=f"Error creating subscription: {str(e)}"  
        )
    else:
        process_subscriptions(db,user)
        return new_subscription
    
def update_subscription(db: Session, user, input_subscription:updated_subscription):
    subscription = db.query(Subscriptions).filter(
        Subscriptions.owner == user.id,
        Subscriptions.id == input_subscription.id
    ).first()

    if not subscription:  
        raise HTTPException(  
            status_code=status.HTTP_404_NOT_FOUND,  
            detail="Subscription not found or not owned by the user"  
        )
    if  not subscription.is_active and input_subscription.is_active:
        subscription.start_date = ensure_timezone_aware(datetime.now())
        subscription.current_count = 0
        flag = 1
        #process_subscriptions(db, user)

    update_data = input_subscription.model_dump(exclude_unset=True,exclude={"id"}) 
    for x,y in update_data.items():
        setattr(subscription,x,y)
    subscription.updated_date = ensure_timezone_aware(datetime.now()) 
    db.commit()
    db.refresh(subscription)
    
    return subscription

   
def process_subscriptions(db: Session, user):  
    current_time = ensure_timezone_aware(datetime.now()) 
    # Get all active subscriptions  
    active_subscriptions = db.query(Subscriptions).filter( 
        Subscriptions.is_active == True,
        Subscriptions.owner == user.id
    ).all()  
      
    for subscription in active_subscriptions:                
        # Check if expense should be generated  
        if should_generate_expense(subscription, current_time, db): 
            generate_subscription_expense(user, subscription, db) 

        # Check if subscription should be deactivated  
        if should_deactivate_subscription(subscription, current_time): 
            subscription.is_active = False  
            db.commit()

def read_subscription(db:Session, user):
    current_subscriptions = db.query(Subscriptions).filter(
        Subscriptions.owner == user.id,
        Subscriptions.is_active == True
    ).all()

    return current_subscriptions

def deactivate_subscription(db:Session, user, id:int):
    subscription = db.query(Subscriptions).filter(
        Subscriptions.owner == user.id,
        Subscriptions.id == id,
        Subscriptions.is_active == True
    ).first()

    if not subscription:
        raise HTTPException(status_code = 404, detail = "Active subscription does not exist")

    subscription.is_active = False
    db.commit()
    db.refresh(subscription)
    return subscription

    
  
def should_deactivate_subscription(subscription: Subscriptions, current_time: datetime) -> bool:   
    # Check end date 
    subscription_end = ensure_timezone_aware(subscription.end_date) 
    if subscription.end_date and current_time >= subscription_end:  
        return True  
      
    # Check repeat count  
    if subscription.repeat_count and subscription.current_count >= subscription.repeat_count:  
        return True  
          
    return False  
  
def should_generate_expense(subscription: Subscriptions, current_time: datetime, db: Session) -> bool:      
    # Calculate how many payments should have been made by now  
    expected_payments = calculate_expected_payments(subscription, current_time)  
      
    # Check how many payments have actually been made  
    actual_payments = db.query(Expenses).filter(  
        Expenses.subscription_id == subscription.id,
        #for cases when status changed deactivated to activated
        extract('day', Expenses.expense_created_date) >= extract('day', subscription.start_date) 
    ).count()  
       
    return actual_payments < expected_payments 
  
def calculate_payment_date(subscription: Subscriptions) -> datetime:  
    """Calculate when the next expense should be generated"""  
      
    if subscription.frequency == FrequencyType.DAILY:  
        return subscription.start_date + timedelta(days=subscription.current_count)  
    elif subscription.frequency == FrequencyType.WEEKLY:  
        return subscription.start_date + timedelta(weeks=subscription.current_count)  
    elif subscription.frequency == FrequencyType.MONTHLY:   
        return subscription.start_date + relativedelta(months = subscription.current_count)                                                
    elif subscription.frequency == FrequencyType.YEARLY:  
        return subscription.start_date + relativedelta(years = subscription.current_count)
    
def generate_subscription_expense(user,subscription: Subscriptions, db: Session):  
    current_time = ensure_timezone_aware(datetime.now())  
      
    # Calculate how many payments should exist  
    expected_payments = calculate_expected_payments(subscription, current_time)  
      
    # Get existing payments  
    existing_payments = db.query(Expenses).filter(  
        Expenses.subscription_id == subscription.id,
        extract('day', Expenses.expense_created_date) >= extract('day', subscription.start_date)  
    ).count()  
      
    # Generate missing payments  
    payments_to_generate = expected_payments - existing_payments  
      
    for i in range(payments_to_generate):  
        # Calculate the date for this specific payment  
        payment_date = calculate_payment_date(subscription)  
          
        expense_data = expense(  
            expense_amount=subscription.amount,  
            expense_category=subscription.category,  
            expense_emoji="🔄️",
            subscription_id = subscription.id
        )  
          
        try:  
            # Create expense with the correct date  
            create_new_expense(user, db, expense_data, subscription_id=subscription.id, expense_created_date=payment_date)  
            subscription.current_count += 1  
            db.commit()  
        except Exception as e:  
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create catch-up expense for subscription {subscription.id}: {str(e)}")
           

def calculate_expected_payments(subscription: Subscriptions, current_time: datetime) -> int:

    subscription_start = ensure_timezone_aware(subscription.start_date)  

    if current_time < subscription_start:
        return 0
    
    time_diff = current_time - subscription_start
    


    if subscription.frequency == FrequencyType.DAILY:
        expected = time_diff.days + 1
    elif subscription.frequency == FrequencyType.WEEKLY:
        expected = (time_diff.days // 7) + 1
    elif subscription.frequency == FrequencyType.MONTHLY:
        expected = calculate_months_between(subscription_start, current_time) + 1
    elif subscription.frequency == FrequencyType.YEARLY:
        expected = calculate_years_between(subscription_start, current_time) + 1
    else:
        expected = 0

    if subscription.repeat_count:
        return min(expected, subscription.repeat_count)
    
    return expected


def calculate_months_between(start_date: datetime, end_date: datetime) -> int:
    #Returns the number of full months between two dates
    rd = relativedelta(end_date, start_date)
    return rd.years * 12 + rd.months

def calculate_years_between(start_date: datetime, end_date: datetime) -> int:
    #Returns the number of full years between two dates
    rd = relativedelta(end_date, start_date)
    return rd.years


def ensure_timezone_aware(dt):  
    #Ensure datetime is timezone-aware with IST  
    if dt and dt.tzinfo is None:  
        ist_tz = timezone(timedelta(hours=5, minutes=30))  
        return dt.replace(tzinfo=ist_tz)  
    return dt  

def create_default_budget(db: Session, user):
    current_subscriptions = db.query(Subscriptions).filter(
        Subscriptions.owner == user.id,
        Subscriptions.is_active == True
    ).all()

    current_month = get_ist_datetime().month  
    current_year = get_ist_datetime().year

    for sub in current_subscriptions:
    
        existing_budget = db.query(Budgets).filter(  
            Budgets.budget_category == sub.category,  
            Budgets.owner == user.id,  
            extract('month', Budgets.budget_created_date) == current_month,  
            extract('year', Budgets.budget_created_date) == current_year  
        ).first()

        if not existing_budget:   
            current_count = sub.current_count

            today = datetime.today()
            first_day_this_month = datetime(today.year, today.month, 1)
            last_day_last_month_date = first_day_this_month - timedelta(days=1)            
            last_day = calendar.monthrange(today.year, today.month)[1]

            last_moment_this_month = datetime(today.year, today.month, last_day, 23, 59, 59)
            last_moment_last_month = datetime(
            last_day_last_month_date.year,
            last_day_last_month_date.month,
            last_day_last_month_date.day,
            23, 59, 59            
            )
            aware_last_moment_last_month = ensure_timezone_aware(last_moment_last_month)
            aware_last_moment_this_month = ensure_timezone_aware(last_moment_this_month)

            count_till_last_month = calculate_expected_payments(sub, ensure_timezone_aware(aware_last_moment_last_month))
            remaining_count = calculate_expected_payments(sub, ensure_timezone_aware(aware_last_moment_this_month)) - count_till_last_month
            amount = sub.amount * remaining_count
            if amount > 0:
                new_default_budget = budget(
                    budget_amount = amount,
                    budget_category = sub.category,
                    budget_emoji = "💳"         
                )
                create_new_budget(db, user, new_default_budget)


