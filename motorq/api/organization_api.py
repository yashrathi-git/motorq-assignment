from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from motorq.deps import get_db
from motorq.models.organizations import Organization
from motorq.schemas.organizations import OrganizationCreate, OrganizationResponse

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