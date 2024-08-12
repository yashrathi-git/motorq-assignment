from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from motorq.helper.decode_vin import decode_vin
from motorq.models.vehicles import Vehicle
from motorq.models.organizations import Organization
from motorq.deps import get_db
from pydantic import BaseModel, Field
import re

from motorq.schemas.vehicles import VehicleCreate

router = APIRouter(prefix="/vehicles", tags=["vehicles"])



@router.post("", status_code=201)
async def create_vehicle(vehicle: VehicleCreate, db: AsyncSession = Depends(get_db)):
    org = await db.get(Organization, vehicle.org)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    try:
        decoded_info = await decode_vin(vehicle.vin)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to decode VIN: {str(e)}")


    db_vehicle = Vehicle(
        vin=vehicle.vin,
        manufacturer=decoded_info['manufacturer'],
        model=decoded_info['model'],
        year=int(decoded_info['year']),
        org_id=vehicle.org
    )

    db.add(db_vehicle)
    await db.commit()
    await db.refresh(db_vehicle)

    return {"message": "Vehicle added successfully", "vehicle": db_vehicle}

@router.get("/decode/{vin}")
async def decode_vin_route(vin: str):
    try:
        vehicle_info = await decode_vin(vin)
        return vehicle_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to decode VIN: {str(e)}")

@router.get("/{vin}")
async def get_vehicle(
    vin: str = Path(..., min_length=17, max_length=17, regex="^[A-HJ-NPR-Z0-9]{17}$"),
    db: AsyncSession = Depends(get_db)
):
    if not re.match("^[A-HJ-NPR-Z0-9]{17}$", vin):
        raise HTTPException(status_code=400, detail="Invalid VIN format")

    vehicle = await db.get(Vehicle, vin)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return vehicle