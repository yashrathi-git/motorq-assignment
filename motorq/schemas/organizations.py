from typing import Optional
from pydantic import BaseModel, Field

class OrganizationCreate(BaseModel):
    name: str
    account: str
    website: str
    fuel_reimbursement_policy: Optional[str] = None
    speed_limit_policy: Optional[str] = None
    parent_org_id: Optional[int] = None

class OrganizationResponse(BaseModel):
    org_id: int
    name: str
    account: str
    website: str
    fuel_reimbursement_policy: Optional[str] = None
    speed_limit_policy: Optional[str] = None
    parent_org_id: Optional[int] = None

    class Config:
        orm_mode = True

class OrganizationUpdate(BaseModel):
    account: Optional[str] = None
    website: Optional[str] = None
    fuel_reimbursement_policy: Optional[str] = None
    speed_limit_policy: Optional[str] = None