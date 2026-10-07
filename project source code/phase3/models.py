from pydantic import BaseModel, Field, field_validator

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
    tenure: int
    monthly_charges: float
    contract_type: str
    service_count: int


    @field_validator("tenure")
    @classmethod
    def validate_tenure(cls, value):
        if value < 0 or value > 100:
            raise ValueError("tenure must be between 0 and 100")
        return value

    @field_validator("monthly_charges")
    @classmethod
    def validate_monthly_charges(cls, value):
        if value <= 0:
            raise ValueError("monthly_charges must be greater than 0")
        return value


class ErrorResponse(BaseModel):
    detail: str
    status_code: int