from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Base:  
    __tablename__ = None

    id = Column(Integer, primary_key=True, index=True)

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, nullable=False)
   

class Vehicle(Base):
    __tablename__ = "vehicles"

    vehicle_id = Column(Integer, nullable=False)
    vehicle_no = Column(String, nullable=False)
    

class VehicleType(Base):
    __tablename__ = "vehicle_types"

    vehicle_type_id = Column(Integer, nullable=False)
    vehicle_type_name = Column(String, nullable=False)
    

class TollPlaza(Base):
    __tablename__ = "toll_plazas"

    toll_plaza_id = Column(Integer, nullable=False)
    toll_plaza_name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    

class PaymentDetail(Base):
    __tablename__ = "payment_details"

    payment_id = Column(Integer, nullable=False)
    

class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    method_id = Column(Integer, nullable=False)
    method_name = Column(String, nullable=False)
   

class GpsTollTransaction(Base):
    __tablename__ = "gps_toll_transactions"

    transaction_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    vehicle_no = Column(String, nullable=False)
    toll_plaza_id = Column(Integer, ForeignKey("toll_plazas.toll_plaza_id"))
    transaction_date = Column(DateTime, nullable=False)
    transaction_time = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    isreturn = Column(Boolean, default=False)
    is_valid = Column(Boolean, nullable=True)
    otp = Column(String, nullable=True)
    is_passed = Column(Boolean, nullable=True)

    user = relationship("User", backref="gps_toll_transactions")
    vehicle = relationship("Vehicle", backref="gps_toll_transactions")
    toll_plaza = relationship("TollPlaza", backref="gps_toll_transactions")
