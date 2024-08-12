from pydantic import BaseModel, Field


class VehicleCreate(BaseModel):
    vin: str = Field(..., min_length=17, max_length=17, pattern="^[A-HJ-NPR-Z0-9]{17}$")
    org: int