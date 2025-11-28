from app.repositories.base_repository import BaseRepository
from app.models.category import Category

class CategoryRepository(BaseRepository):
    model = Category

    @classmethod
    def get_by_slug(cls, slug):
        return cls.model.query.filter_by(slug=slug).first()

    @classmethod
    def get_all_active_ordered(cls):
        return cls.model.query.filter_by(is_active=True).order_by(cls.model.display_order).all()

    @classmethod
    def create_with_slug(cls, slug, name_en, name_bg, **kwargs):
        return cls.create(slug=slug, name_en=name_en, name_bg=name_bg, **kwargs)
