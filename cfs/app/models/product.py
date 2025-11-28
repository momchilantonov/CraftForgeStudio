from datetime import datetime, timezone
from app.extensions import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name_en = db.Column(db.String(200), nullable=False)
    name_bg = db.Column(db.String(200), nullable=False)
    description_en = db.Column(db.Text)
    description_bg = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    stock = db.Column(db.Integer, default=0, nullable=False)
    image_url = db.Column(db.String(255))
    additional_images = db.Column(db.JSON)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_featured = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    category = db.relationship('Category', back_populates='products')

    def get_name(self, lang='en'):
        return self.name_en if lang == 'en' else self.name_bg

    def get_description(self, lang='en'):
        return self.description_en if lang == 'en' else self.description_bg

    @property
    def in_stock(self):
        return self.stock > 0

    def __repr__(self):
        return f'<Product {self.sku}>'
