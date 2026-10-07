from fastapi.middleware.cors import CORSMiddleware

from fastapi import Depends, FastAPI,HTTPException,Query

from sqlalchemy import create_engine,text
from sqlalchemy.orm import Session, sessionmaker

from models import CustomerResponse, CustomerFeatures,ChurnPredictionRequest

from servicelayer import get_churn_summary, get_customer_features,get_high_risk_customers
from predict import predict_churn as generate_churn_prediction

app = FastAPI()

engine = create_engine("mysql+pymysql://root:root@localhost:3306/cris")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/customers/high-risk")
def high_risk_customers(
    limit: int = Query(default=50, ge=1),
    min_tenure: int | None = None,
    max_tenure: int | None = None,  
     
):
    print("High Risk Customers Endpoint called")
    return get_high_risk_customers(
        db=db,
        limit=limit,
        min_tenure=min_tenure,
        max_tenure=max_tenure
    )


@app.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: str):
    customer = db.execute(text(
        "select c.customer_id, fca.tenure, dc.contract_name as contract_type, scr.internet_service, fca.monthly_charges, fca.churn from customers c " \
        "join fact_customer_account fca on c.customer_id = fca.customer_id " \
        "join dim_contract dc on fca.contract_key = dc.contract_key " \
        "join stg_customer_raw scr on c.customer_id = scr.customer_id " \
        "where c.customer_id = :customer_id"),
        {"customer_id": customer_id}

    ).fetchone()

    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    return CustomerResponse(
        customer_id=customer.customer_id,
        tenure=customer.tenure,
        contract_type=customer.contract_type,
        internet_service=customer.internet_service,
        monthly_charges=customer.monthly_charges,
        churn=customer.churn
    )


@app.get("/churn/summary")
def churn_summary():
        print("summary Endpoint called")
        return get_churn_summary(db)






@app.get("/customer/{customer_id}/features",
    response_model=CustomerFeatures
)
def customer_features(
    customer_id: str
):
    return get_customer_features(db, customer_id)


@app.post("/predict-churn")
def predict_churn(request: ChurnPredictionRequest):

    result = generate_churn_prediction(
        tenure=request.tenure,
        monthly_charges=request.monthly_charges,
        contract_type=request.contract_type,
        service_count=request.service_count,
        internet_service = request.internet_service
    )    

    return result


