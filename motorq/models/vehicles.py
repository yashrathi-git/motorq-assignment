from sqlalchemy import Column, String, Integer, ForeignKey, Numeric
from motorq.models import Base
from sqlalchemy.orm import relationship


class Vehicle(Base):
    __tablename__ = "vehicles"

    vin = Column(String(17), primary_key=True)
    manufacturer = Column(String(100))
    model = Column(String(100))
    year = Column(Integer)
    org_id = Column(Integer, ForeignKey('organizations.org_id'))

    organization = relationship("Organization", back_populates="vehicles")