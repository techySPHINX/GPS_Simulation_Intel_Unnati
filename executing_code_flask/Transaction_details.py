from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from executing_code_flask.connection import DATABASE_URL
from .model import User, Vehicle, TollPlaza, VehicleType, PaymentDetail, PaymentMethod

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Transaction:

    def __init__(self, db):
        self.db = db

    def get_transaction_by_user_id(self, user_id):
        # Used for receiving transaction details for further communication using user ID
        session = self.db.session

        try:
            results = session.query(Transaction, User.user_name, Vehicle.vehicle_no, VehicleType.vehicle_type_name, TollPlaza.toll_plaza_id, TollPlaza.city, PaymentMethod.method_name) \
                .join(User, Transaction.user_id == User.user_id) \
                .join(Vehicle, Transaction.vehicle_no == Vehicle.vehicle_no) \
                .join(VehicleType, Vehicle.vehicle_type_id == VehicleType.vehicle_type_id) \
                .join(TollPlaza, Transaction.toll_plaza_id == TollPlaza.toll_plaza_id) \
                .join(PaymentDetail, Transaction.payment_id == PaymentDetail.payment_id) \
                .join(PaymentMethod, PaymentDetail.method_id == PaymentMethod.method_id) \
                .filter(Transaction.user_id == user_id) \
                .all()
            return results
        except Exception as e:
            print("Error fetching transactions by user:", e)
            return None
        finally:
            session.close()

    def add_transaction(self, transaction_data):
        # Update Transaction for system backup
        session = self.db.session

        try:
            new_transaction = Transaction(
                user_id=transaction_data["user_id"],
                payment_id=transaction_data["payment_id"],
                vehicle_no=transaction_data["vehicle_no"],
                toll_plaza_id=transaction_data["toll_plaza_id"],
                transaction_date=transaction_data["transaction_date"],
                transaction_time=transaction_data["transaction_time"],
                status=transaction_data["status"],
                amount=transaction_data["amount"],
                isreturn=transaction_data["isreturn"],
                isValid=transaction_data.get("isValid", None),
                otp=transaction_data.get("otp", None),
                isPassed=transaction_data.get("isPassed", None),
            )
            session.add(new_transaction)
            session.commit()
            return new_transaction
        except Exception as e:

            print("Error adding transaction:", e)
            session.rollback()
            return None
        finally:
            session.close()

    def get_transaction_by_id(self, id):
        # Details of all vehicles through vehicle ID
        session = self.db.session

        try:
            result = session.query(Transaction, User.user_name, Vehicle.vehicle_no, VehicleType.vehicle_type_name, TollPlaza.toll_plaza_id, TollPlaza.city, PaymentMethod.method_name) \
                .join(User, Transaction.user_id == User.user_id) \
                .join(Vehicle, Transaction.vehicle_no == Vehicle.vehicle_no) \
                .join(VehicleType, Vehicle.vehicle_type_id == VehicleType.vehicle_type_id) \
                .join(TollPlaza, Transaction.toll_plaza_id == TollPlaza.toll_plaza_id) \
                .join(PaymentDetail, Transaction.payment_id == PaymentDetail.payment_id) \
                .join(PaymentMethod, PaymentDetail.method_id == PaymentMethod.method_id) \
                .filter(Transaction.transaction_id == id) \
                .first()
            return result
        except Exception as e:
            
            print("Error fetching transaction by ID:", e)
            return None
