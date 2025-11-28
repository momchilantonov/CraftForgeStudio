from app.repositories.base_repository import BaseRepository
from app.models.order import Order
from datetime import datetime
import secrets

class OrderRepository(BaseRepository):
    model = Order

    @classmethod
    def get_by_order_number(cls, order_number):
        return cls.model.query.filter_by(order_number=order_number).first()

    @classmethod
    def generate_order_number(cls):
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        random_suffix = secrets.token_hex(4).upper()
        return f'CFS-{timestamp}-{random_suffix}'

    @classmethod
    def create_order(cls, full_name, email, phone, delivery_method, delivery_address,
                     payment_method, subtotal, shipping, total, items):
        order_number = cls.generate_order_number()
        return cls.create(
            order_number=order_number,
            full_name=full_name,
            email=email,
            phone=phone,
            delivery_method=delivery_method,
            delivery_address=delivery_address,
            payment_method=payment_method,
            subtotal=subtotal,
            shipping=shipping,
            total=total,
            items=items
        )

    @classmethod
    def get_recent(cls, limit=10):
        return cls.model.query.order_by(cls.model.created_at.desc()).limit(limit).all()

    @classmethod
    def get_by_status(cls, status):
        return cls.model.query.filter_by(status=status).order_by(cls.model.created_at.desc()).all()
