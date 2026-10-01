from datetime import datetime

from pydantic import BaseModel, Field, field_validator,model_validator

from config.interests import MAX_INTERESTS,VALID_INTEREST_VALUES
from tools.airport_tools import STATE_REGION_CODES, get_airport

DATE_FORMAT = "%d-%m-%Y"

class TripRequest(BaseModel):
    origin_airport: str
    budget: float = Field(gt=0)
    currency: str = "INR"
    start_date: str
    end_date: str 
    travelers: int = Field(ge=1, le=9)
    interests: list[str] = Field(min_length=1, max_length=MAX_INTERESTS)
    allowed_state: str = ""

    @field_validator("origin_airport")
    @classmethod
    def validate_origin(cls, v: str):
        if not get_airport(v):
            raise ValueError("Invalid Origin Airport")
        return v.strip().upper()

    @field_validator("interests")
    @classmethod
    def validate_interest(cls, values: list[str]):
        invalid = [v for v in values if v not in VALID_INTEREST_VALUES]
        if invalid:
            raise ValueError(f"Invalid interest: {invalid}")
        return values

    @field_validator("allowed_state")
    @classmethod
    def validate_state(cls, v: str):
        if v and v not in STATE_REGION_CODES:
            raise ValueError("Invalid States")
        return v

    @model_validator(mode="after")
    def validate_dates(self):
        start = datetime.strptime(self.start_date, DATE_FORMAT)
        end = datetime.strptime(self.end_date,DATE_FORMAT)

        if end <= start:
            raise ValueError("end date must be after start date")

        return self

    

