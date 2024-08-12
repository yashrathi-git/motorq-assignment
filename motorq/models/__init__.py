from sqlalchemy.orm import declarative_base

Base = declarative_base()

from motorq.models.vehicles import Vehicle
from motorq.models.organizations import Organization