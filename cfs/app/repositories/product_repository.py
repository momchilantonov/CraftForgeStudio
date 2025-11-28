from app.repositories.base_repository import BaseRepository
from app.models.product import Product

class ProductRepository(BaseRepository):
    model = Product

    @classmethod
    def get_by_sku(cls, sku):
        return cls.model.query.filter_by(sku=sku).first()

    @classmethod
    def get_by_category(cls, category_id, active_only=True):
        query = cls.model.query.filter_by(category_id=category_id)
        if active_only:
            query = query.filter_by(is_active=True)
        return query.all()

    @classmethod
    def get_featured(cls, limit=4):
        return cls.model.query.filter_by(is_featured=True, is_active=True).limit(limit).all()

    @classmethod
    def search(cls, search_term, category_id=None):
        query = cls.model.query.filter(
            cls.model.is_active == True,
            (cls.model.name_en.ilike(f'%{search_term}%')) |
            (cls.model.name_bg.ilike(f'%{search_term}%'))
        )
        if category_id:
            query = query.filter_by(category_id=category_id)
        return query.all()

    @classmethod
    def get_paginated(cls, page=1, per_page=12, category_id=None):
        query = cls.model.query.filter_by(is_active=True)
        if category_id:
            query = query.filter_by(category_id=category_id)
        return query.paginate(page=page, per_page=per_page, error_out=False)
