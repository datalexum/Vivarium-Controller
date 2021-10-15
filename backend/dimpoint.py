from pydantic import BaseModel, ValidationError, validator, Field
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer

Base = declarative_base()


class DimPoint(BaseModel):
    hour: int = Field(
        title="Time hour",
        description="Hour as part of the time setting",
        gt=0,
        le=23
    )
    minute: int = Field(
        title="Time minute",
        description="Minute as part of the time setting",
        ge=0,
        le=59
    )
    percent: int = Field(
        title="Light intensity",
        description="Light intensity in percent (%)",
        ge=0,
        le=100
    )

    def toOrm(self):
        return DimPointORM(hour=self.hour, minute=self.minute, percent=self.percent)

    class Config:
        orm_mode = True


class DimPointORM(Base):
    __tablename__ = 'dim_points'
    id = Column(Integer, primary_key=True, nullable=False)
    hour = Column(Integer, nullable=False)
    minute = Column(Integer, nullable=False)
    percent = Column(Integer, nullable=False)
