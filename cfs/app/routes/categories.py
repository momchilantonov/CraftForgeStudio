from app.repositories.base_repository import BaseRepository
from app.models.category import Category


class CategoryRepository(BaseRepository):
    model = Category

    @classmethod
    def get_by_slug(cls, slug):
        return cls.model.query.filter_by(slug=slug, is_active=True).first()

    @classmethod
    def get_all_active_ordered(cls):
        return cls.model.query.filter_by(is_active=True).order_by(cls.model.display_order).all()

    @classmethod
    def get_main_categories_ordered(cls):
        return cls.model.query.filter_by(is_active=True, parent_id=None).order_by(cls.model.display_order).all()

    @classmethod
    def get_subcategories_by_parent(cls, parent_id):
        return cls.model.query.filter_by(is_active=True, parent_id=parent_id).order_by(cls.model.display_order).all()

    @classmethod
    def get_category_tree(cls):
        main_categories = cls.get_main_categories_ordered()
        tree = []
        for main_cat in main_categories:
            tree.append({
                'category': main_cat,
                'subcategories': list(main_cat.subcategories.filter_by(is_active=True).order_by(cls.model.display_order))
            })
        return tree

    @classmethod
    def create_with_slug(cls, slug, **kwargs):
        obj = cls.model(slug=slug, **kwargs)
        return cls.save(obj)

    @classmethod
    def create_subcategory(cls, parent_id, slug, **kwargs):
        parent = cls.get_by_id(parent_id)
        if not parent or parent.is_subcategory():
            raise ValueError("Invalid parent category")
        kwargs['parent_id'] = parent_id
        kwargs['level'] = 1
        return cls.create_with_slug(slug, **kwargs)
