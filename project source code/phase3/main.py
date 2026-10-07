from fastapi import Depends, FastAPI,HTTPException,Query, Request,Header

from sqlalchemy import create_engine,text
from sqlalchemy.orm import Session, sessionmaker

from models import CustomerResponse, CustomerFeatures,ChurnPredictionRequest,ErrorResponse

from servicelayer import get_churn_summary, get_customer_features,get_high_risk_customers

from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from sqlalchemy.exc import SQLAlchemyError

import os
import logging



engine = create_engine("mysql+pymysql://root:root@localhost:3306/cris")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()

app = FastAPI()

# -------------------------
# Logging
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# -------------------------
# API Key
# -------------------------
API_KEY = os.getenv("API_KEY")

api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False
)

if not API_KEY:
    logger.warning("API_KEY environment variable is not set")





def verify_api_key(
    api_key: str | None = Depends(api_key_header)
):
    if api_key is None or api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )

    return api_key

@app.middleware("http")
async def log_requests(request: Request, call_next):

    logger.info(
        "Incoming request: method=%s path=%s query_params=%s",
        request.method,
        request.url.path,
        dict(request.query_params)
    )

    try:
        response = await call_next(request)

        logger.info(
            "Response: method=%s path=%s status=%s",
            request.method,
            request.url.path,
            response.status_code
        )

        return response

    except Exception:
        logger.exception(
            "Unhandled exception: method=%s path=%s",
            request.method,
            request.url.path
        )
        raise

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):

    logger.warning(
        "404 Not Found: method=%s path=%s",
        request.method,
        request.url.path
    )

    return JSONResponse(
        status_code=404,
        content={
            "detail": "Route not found",
            "status_code": 404
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException
):

    logger.warning(
        "HTTP error: method=%s path=%s status=%s detail=%s",
        request.method,
        request.url.path,
        exc.status_code,
        exc.detail
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": str(exc.detail),
            "status_code": exc.status_code
        }
    )










@app.get(
    "/customers/high-risk",
    response_model=list
)
def high_risk_customers(
    limit: int = Query(default=50, ge=1),
    min_tenure: int | None = None,
    max_tenure: int | None = None,
    api_key: str = Depends(verify_api_key)
):

    logger.info(
        "High-risk request: limit=%s min_tenure=%s max_tenure=%s",
        limit,
        min_tenure,
        max_tenure
    )

    try:

        return get_high_risk_customers(
            db=db,
            limit=limit,
            min_tenure=min_tenure,
            max_tenure=max_tenure
        )

    except SQLAlchemyError:

        logger.exception(
            "Database error while fetching high-risk customers"
        )

        raise HTTPException(
            status_code=500,
            detail="Database unavailable"
        )


    

@app.get(
    "/customers/{customer_id}",
    response_model=CustomerResponse,
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
        401: {"model": ErrorResponse}
    }
)
def get_customer(
    customer_id: str,
    api_key: str = Depends(verify_api_key)
):

    logger.info(
        "Fetching customer: customer_id=%s",
        customer_id
    )

    try:

        customer = db.execute(
            text(
                """
                SELECT
                    c.customer_id,
                    fca.tenure,
                    dc.contract_name AS contract_type,
                    scr.internet_service,
                    fca.monthly_charges,
                    fca.churn
                FROM customers c
                JOIN fact_customer_account fca
                    ON c.customer_id = fca.customer_id
                JOIN dim_contract dc
                    ON fca.contract_key = dc.contract_key
                JOIN stg_customer_raw scr
                    ON c.customer_id = scr.customer_id
                WHERE c.customer_id = :customer_id
                """
            ),
            {"customer_id": customer_id}
        ).fetchone()

        if customer is None:

            logger.warning(
                "Customer not found: customer_id=%s",
                customer_id
            )

            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        return CustomerResponse(
            customer_id=customer.customer_id,
            tenure=customer.tenure,
            contract_type=customer.contract_type,
            internet_service=customer.internet_service,
            monthly_charges=customer.monthly_charges,
            churn=customer.churn
        )

    except SQLAlchemyError:

        logger.exception(
            "Database error while fetching customer: %s",
            customer_id
        )

        raise HTTPException(
            status_code=500,
            detail="Database unavailable"
        )

    finally:
        db.close()



@app.get(
    "/churn/summary",
    responses={
        500: {"model": ErrorResponse},
        401: {"model": ErrorResponse}
    }
)
def churn_summary(
    api_key: str = Depends(verify_api_key)
):

    logger.info("Churn summary endpoint called")

    try:

        return get_churn_summary(db)

    except SQLAlchemyError:

        logger.exception(
            "Database error while fetching churn summary"
        )

        raise HTTPException(
            status_code=500,
            detail="Database unavailable"
        )




@app.get(
    "/customer/{customer_id}/features",
    response_model=CustomerFeatures,
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
        401: {"model": ErrorResponse}
    }
)
def customer_features(
    customer_id: str,
    api_key: str = Depends(verify_api_key)
):

    logger.info(
        "Customer features request: customer_id=%s",
        customer_id
    )

    try:

        return get_customer_features(
            db,
            customer_id
        )

    except SQLAlchemyError:

        logger.exception(
            "Database error while fetching features: customer_id=%s",
            customer_id
        )

        raise HTTPException(
            status_code=500,
            detail="Database unavailable"
        )

@app.post(
    "/predict-churn",
    responses={
        401: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
def predict_churn(
    request: ChurnPredictionRequest,
    api_key: str = Depends(verify_api_key)
):

    logger.info(
        "Churn prediction request: tenure=%s monthly_charges=%s",
        request.tenure,
        request.monthly_charges
    )

    try:

        return {
            "customer_id": "N/A",
            "risk_score": 0.78,
            "prediction": "Likely to churn",
            "note": "stub — real model in ML4"
        }

    except Exception:

        logger.exception(
            "Error while predicting churn"
        )

        raise HTTPException(
            status_code=500,
            detail="Prediction service unavailable"
        )