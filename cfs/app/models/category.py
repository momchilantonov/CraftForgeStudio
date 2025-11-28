from datetime import datetime, timezone
from app.extensions import db

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name_en = db.Column(db.String(100), nullable=False)
    name_bg = db.Column(db.String(100), nullable=False)
    description_en = db.Column(db.Text)
    description_bg = db.Column(db.Text)
    icon = db.Column(db.String(50))
    image_url = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    products = db.relationship('Product', back_populates='category', lazy='dynamic')

    def get_name(self, lang='en'):
        return self.name_en if lang == 'en' else self.name_bg

    def get_description(self, lang='en'):
        return self.description_en if lang == 'en' else self.description_bg

    def __repr__(self):
        return f'<Category {self.slug}>'
