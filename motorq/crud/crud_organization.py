from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from motorq.models.organizations import Organization
from motorq.schemas.organizations import OrganizationCreate, OrganizationUpdate

class CRUDOrganization:

    @staticmethod
    async def create(db: AsyncSession, org: OrganizationCreate) -> Organization:
        db_org = Organization(**org.dict())
        db.add(db_org)
        await db.commit()
        await db.refresh(db_org)
        return db_org

    @staticmethod
    async def get(db: AsyncSession, org_id: int) -> Organization:
        result = await db.execute(select(Organization).filter(Organization.org_id == org_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def update(db: AsyncSession, org_id: int, org_update: OrganizationUpdate) -> Organization:
        db_org = await CRUDOrganization.get(db, org_id)
        if db_org:
            update_data = org_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_org, key, value)
            await db.commit()
            await db.refresh(db_org)
        return db_org

    @staticmethod
    async def delete(db: AsyncSession, org_id: int) -> bool:
        db_org = await CRUDOrganization.get(db, org_id)
        if db_org:
            await db.delete(db_org)
            await db.commit()
            return True
        return False

    @staticmethod
    async def get_organization_details(db: AsyncSession, org_id: int):
        org = await CRUDOrganization.get(db, org_id)
        if not org:
            return None

        org_data = {
            "org_id": org.org_id,
            "name": org.name,
            "account": org.account,
            "website": org.website,
            "parent_org_id": org.parent_org_id
        }

        org_data["fuel_reimbursement_policy"] = await CRUDOrganization._get_inherited_policy(db, org, "fuel_reimbursement_policy")
        org_data["speed_limit_policy"] = await CRUDOrganization._get_inherited_policy(db, org, "speed_limit_policy")

        return org_data

    @staticmethod
    async def _get_inherited_policy(db: AsyncSession, org: Organization, policy_name: str):
        current_org = org
        while current_org:
            policy_value = getattr(current_org, policy_name)
            if policy_value:
                return policy_value
            if current_org.parent_org_id:
                current_org = await CRUDOrganization.get(db, current_org.parent_org_id)
            else:
                break
        return None

    @staticmethod
    async def get_multiple(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Organization]:
        result = await db.execute(select(Organization).offset(skip).limit(limit))
        return result.scalars().all()
    