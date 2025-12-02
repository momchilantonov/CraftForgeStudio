from app.repositories.category_repository import CategoryRepository
from app.utils.helpers import generate_slug


class CategoryService:

    @staticmethod
    def create_category(name_en, name_bg, description_en=None, description_bg=None,
                        parent_id=None, icon=None, image_url=None, display_order=0, is_active=True):
        slug = generate_slug(name_en)

        if parent_id:
            return CategoryRepository.create_subcategory(
                parent_id=parent_id,
                slug=slug,
                name_en=name_en,
                name_bg=name_bg,
                description_en=description_en,
                description_bg=description_bg,
                icon=icon,
                image_url=image_url,
                display_order=display_order,
                is_active=is_active
            )

        return CategoryRepository.create_with_slug(
            slug=slug,
            name_en=name_en,
            name_bg=name_bg,
            description_en=description_en,
            description_bg=description_bg,
            parent_id=None,
            level=0,
            icon=icon,
            image_url=image_url,
            display_order=display_order,
            is_active=is_active
        )

    @staticmethod
    def update_category(category_id, name_en, name_bg, description_en=None, description_bg=None,
                        parent_id=None, icon=None, image_url=None, display_order=0, is_active=True):
        category = CategoryRepository.get_by_id(category_id)
        if not category:
            return None

        slug = generate_slug(name_en)

        level = 0
        if parent_id:
            parent = CategoryRepository.get_by_id(parent_id)
            if parent and not parent.is_subcategory():
                level = 1

        return CategoryRepository.update(category,
                                         slug=slug,
                                         name_en=name_en,
                                         name_bg=name_bg,
                                         description_en=description_en,
                                         description_bg=description_bg,
                                         parent_id=parent_id,
                                         level=level,
                                         icon=icon,
                                         image_url=image_url,
                                         display_order=display_order,
                                         is_active=is_active
                                         )

    @staticmethod
    def delete_category(category_id):
        category = CategoryRepository.get_by_id(category_id)
        if not category:
            return False

        if category.products.count() > 0:
            return False

        if category.subcategories.count() > 0:
            return False

        return CategoryRepository.delete(category)

    @staticmethod
    def get_all_categories():
        return CategoryRepository.get_all()

    @staticmethod
    def get_main_categories():
        return CategoryRepository.get_main_categories_ordered()

    @staticmethod
    def get_category_by_id(category_id):
        return CategoryRepository.get_by_id(category_id)
