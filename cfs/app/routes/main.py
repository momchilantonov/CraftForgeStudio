from flask import Blueprint, render_template, session
from app.repositories.product_repository import ProductRepository
from app.repositories.category_repository import CategoryRepository

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    lang = session.get('language', 'en')

    featured_products = ProductRepository.get_featured(limit=4)
    categories = CategoryRepository.get_all_active_ordered()

    template = f'pages/home_{lang}.html'

    return render_template(
        template,
        featured_products=featured_products,
        categories=categories
    )
