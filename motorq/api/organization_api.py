from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from motorq.deps import get_db
from motorq.models.organizations import Organization
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
    for key, value in update_data.items():
        setattr(org, key, value)

    await db.commit()
    await db.refresh(org)

    return org