from sqlalchemy import Column, Integer, String, Text
from database import Base

# Database model
class Samples(Base):
    __tablename__ = 'samples'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    # filename = Column(String, nullable=False)
