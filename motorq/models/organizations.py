
from sqlalchemy import Column, String, Integer, ForeignKey, Numeric
from motorq.models import Base
from sqlalchemy.orm import relationship


class Organization(Base):
    __tablename__ = "organizations"

    org_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    account = Column(String(100))
    website = Column(String(100))
    fuel_reimbursement_policy = Column(String(100), default="Policy 1000")
    speed_limit_policy = Column(String(100))
    parent_org_id = Column(Integer, ForeignKey('organizations.org_id'), nullable=True)

    vehicles = relationship("Vehicle", back_populates="organization")
    parent_org = relationship("Organization", remote_side=[org_id], backref="child_orgs")
