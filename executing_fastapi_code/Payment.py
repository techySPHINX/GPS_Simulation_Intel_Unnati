import sys
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import executing_code_flask.Payment_Deduction as Payment_Deduction

from executing_code_flask.connection import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define ORM base class
Base = declarative_base()

# PaymentDetail model
class PaymentDetail(Base):
    __tablename__ = "payment_detail"

    payment_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    method_id = Column(Integer, ForeignKey('payment_method.method_id'))
    card_no = Column(String)
    expiry_month = Column(String)
    expiry_year = Column(String)
    card_name = Column(String)


class Payment:

    def __init__(self, db):
        self.db = db

    def get_all_payments(self):
        # Payments of all vehicles information < like Balanced sheet >
        session = self.db.session

        try:
            results = session.query(PaymentDetail).all()
            return results
        except Exception as e:

            print("Error fetching all payments:", e)
            return None
        finally:
            session.close()

    def get_payment_detail_by_id(self, id):
        # Here this app is also connected to user through central administration to retreive data through Payment.ID
        session = self.db.session

        try:
            result = session.query(PaymentDetail).filter_by(
                payment_id=id).first()
            return result
        except Exception as e:

            print("Error fetching payment detail by ID:", e)
            return None
        finally:
            session.close()

    def add_payment(self, payment_data):
        # Here we can allow user to pay manually through connecting to our database 
        # and it must be informed to system and server get updated
        session = self.db.session

        try:
            new_payment = PaymentDetail(
                user_id=payment_data["user_id"],
                method_id=payment_data["method_id"],
                card_no=payment_data["card_no"],
                expiry_month=payment_data["expiry_month"],
                expiry_year=payment_data["expiry_year"],
                card_name=payment_data["card_name"]
            )
            session.add(new_payment)
            session.commit()
            return new_payment
        except Exception as e:

            print("Error adding payment:", e)
            session.rollback()
            return None
        finally:
            session.close()

    def get_payment_detail_by_user(self, user_id):
        # App made for users to get Payment Details through user_id
        session = self.db.session

        try:
            results = session.query(PaymentDetail).filter_by(
                user_id=user_id).all()
            return results
        except Exception as e:

            print("Error fetching payment details by user:", e)
            return None
        finally:
            session.close()

    def update_payment_by_id(self, payment_data):
        # User are also allowed to make update of their transaction by connecting to server through online by using user_id
        session = self.db.session

        try:
            payment = session.query(PaymentDetail).filter_by(
                payment_id=payment_data["payment_id"]).first()
            if payment:
                payment.user_id = payment_data["user_id"]
                payment.method_id = payment_data["method_id"]
                payment.card_no = payment_data["card_no"]
                payment.expiry_month = payment_data["expiry_month"]
                payment.expiry_year = payment_data["expiry_year"]
                payment.card_name = payment_data["card_name"]
                session.commit()
                return payment
            else:
                print("Payment with ID",
                      payment_data["payment_id"], "not found")
                return None
        except Exception as e:

            print("Error updating payment:", e)
