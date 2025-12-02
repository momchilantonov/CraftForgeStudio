from datetime import datetime, timezone
from app.extensions import db


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    name_en = db.Column(db.String(100), nullable=False)
    name_bg = db.Column(db.String(100), nullable=False)
    description_en = db.Column(db.Text)
    description_bg = db.Column(db.Text)
    icon = db.Column(db.String(50))
    image_url = db.Column(db.String(255))
    parent_id = db.Column(db.Integer, db.ForeignKey(
        'categories.id'), nullable=True, index=True)
    level = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    display_order = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(
        timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(
        timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    parent = db.relationship('Category', remote_side=[id], backref=db.backref(
        'subcategories', lazy='dynamic', order_by='Category.display_order'))
    products = db.relationship('Product', backref='category', lazy='dynamic')

    def get_name(self, lang='en'):
        return self.name_en if lang == 'en' else self.name_bg

    def get_description(self, lang='en'):
        return self.description_en if lang == 'en' else self.description_bg

    def is_main_category(self):
        return self.parent_id is None

    def is_subcategory(self):
        return self.parent_id is not None

    def get_full_path(self, lang='en'):
        if self.is_main_category():
            return self.get_name(lang)
        return f"{self.parent.get_name(lang)} > {self.get_name(lang)}"

    def __repr__(self):
        return f'<Category {self.name_en}>'
