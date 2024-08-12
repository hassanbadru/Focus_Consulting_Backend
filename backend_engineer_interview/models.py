import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey


class Base(DeclarativeBase):
    """
    Base sqlalchemy model that all downstream models inherit from
    """
    pass


class Employee(Base):
    __tablename__: str = "employee"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    date_of_birth: Mapped[datetime.date]
    secret: Mapped[str]

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    
class LeaveApplication(Base):
    __tablename__: str = "leave_application"
    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id = mapped_column(Integer, ForeignKey("employee.id"))
    employee = relationship("Employee", foreign_keys=[employee_id])
    leave_start_date: Mapped[str]
    leave_end_date: Mapped[str]
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}