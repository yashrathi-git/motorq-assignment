from typing import Optional
from pydantic import BaseModel, Field

class OrganizationCreate(BaseModel):
    name: str
    account: str
    website: str
    fuel_reimbursement_policy: str = Field(default="Policy 1000")
    speed_limit_policy: str
    parent_org_id: Optional[int] = None

class OrganizationResponse(BaseModel):
    org_id: int
    name: str
    account: str
    website: str
    fuel_reimbursement_policy: str
    speed_limit_policy: str
    parent_org_id: Optional[int]

    class Config:
        orm_mode = True