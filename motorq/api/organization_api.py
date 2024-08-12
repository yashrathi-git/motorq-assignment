from typing import List
from fastapi import APIRouter, HTTPException, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from motorq.crud.crud_organization import CRUDOrganization
from motorq.deps import get_db
from motorq.models.organizations import Organization
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from motorq.schemas.organizations import OrganizationCreate, OrganizationResponse, OrganizationUpdate

router = APIRouter(prefix="/Orgs", tags=["organizations"])

@router.post("", response_model=OrganizationResponse, status_code=201)
async def create_organization(org: OrganizationCreate, db: AsyncSession = Depends(get_db)):
    db_org = Organization(**org.dict())
    
    if org.parent_org_id is not None:
        parent_org = await db.get(Organization, org.parent_org_id)
        if parent_org is None:
            raise HTTPException(status_code=404, detail="Parent organization not found")
    
    db.add(db_org)
    await db.commit()
    await db.refresh(db_org)
    return db_org

async def propagate_fuel_policy(db: AsyncSession, parent_org: Organization, new_policy: str):
    stmt = select(Organization).where(Organization.parent_org_id == parent_org.org_id)
    result = await db.execute(stmt)
    child_orgs = result.scalars().all()

    for child_org in child_orgs:
        child_org.fuel_reimbursement_policy = new_policy
        await propagate_fuel_policy(db, child_org, new_policy)


@router.patch("/{org_id}", response_model=OrganizationResponse)
async def update_organization(
    org_update: OrganizationUpdate,
    org_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db)
):
    org = await db.get(Organization, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    update_data = org_update.dict(exclude_unset=True)
    # IF The parent have already set some value
    # The Child can't update the value
    if 'fuel_reimbursement_policy' in update_data:
        if org.parent_org_id:
            parent_org = await db.get(Organization, org.parent_org_id)
            if parent_org and parent_org.fuel_reimbursement_policy:
                raise HTTPException(
                    status_code=400,
                    detail="The fuel reimbursement policy can't be updated because the parent organization already has a policy set"
                )
            
    for key, value in update_data.items():
        setattr(org, key, value)
    
    if 'fuel_reimbursement_policy' in update_data:
        await propagate_fuel_policy(db, org, update_data['fuel_reimbursement_policy'])

    await db.commit()
    await db.refresh(org)

    return org

@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization(org_id: int = Path(..., gt=0), db: AsyncSession = Depends(get_db)):
    org_details = await CRUDOrganization.get_organization_details(db, org_id)
    if not org_details:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org_details

@router.get("", response_model=List[OrganizationResponse])
async def get_organizations(
    skip: int = Query(0, ge=0),
    limit: int = Query(4, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    organizations = await CRUDOrganization.get_multiple(db, skip=skip, limit=limit)
    return organizations