from pydantic import BaseModel,Field

class CustomerResponse(BaseModel):
    customer_id: str
    tenure: int
    contract_type: str
    internet_service: str
    monthly_charges: float
    churn: bool


class CustomerFeatures(BaseModel):
    customer_id: str
    services_count: int
    high_charge_flag: bool
    is_long_term_contract: bool
    auto_pay_flag: bool
    monthly_charges: float
    total_charges: float



class ChurnPredictionRequest(BaseModel):
    tenure: int = Field(..., ge=0)
    monthly_charges: float = Field(..., ge=0)
    contract_type: str
    service_count: int = Field(..., ge=0, le=6),
    internet_service: str

