from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models.admin import Admin
from app.models.category import Category
from app.models.product import Product
from app.models.order import Order
from app.forms.admin_forms import LoginForm, CategoryForm, ProductForm, UpdateProfileForm, ChangePasswordForm
from app.services.category_service import CategoryService
from app.repositories.product_repository import ProductRepository
from app.repositories.order_repository import OrderRepository
from app.utils.helpers import generate_sku, save_product_image, delete_product_image
from app.extensions import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))

    lang = session.get('language', 'en')
    form = LoginForm()

    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()

        if admin and admin.check_password(form.password.data):
            if not admin.is_active:
                flash('Account is deactivated' if lang ==
                      'en' else 'Акаунтът е деактивиран', 'error')
                return redirect(url_for('admin.login'))

            login_user(admin, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('admin.dashboard'))

        flash('Invalid email or password' if lang ==
              'en' else 'Невалиден имейл или парола', 'error')

    template = f'pages/admin/login_{lang}.html'
    return render_template(template, form=form)


@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    lang = session.get('language', 'en')

    total_products = Product.query.count()
    total_categories = Category.query.count()
    total_orders = Order.query.count()
    recent_orders = OrderRepository.get_recent(limit=5)

    template = f'pages/admin/dashboard_{lang}.html'
    return render_template(template,
                           total_products=total_products,
                           total_categories=total_categories,
                           total_orders=total_orders,
                           recent_orders=recent_orders)


@admin_bp.route('/categories')
@login_required
def categories():
    lang = session.get('language', 'en')
    all_categories = CategoryService.get_all_categories()

    template = f'pages/admin/categories_{lang}.html'
    return render_template(template, categories=all_categories)


@admin_bp.route('/categories/add', methods=['GET', 'POST'])
@login_required
def add_category():
    lang = session.get('language', 'en')
    form = CategoryForm()

    main_categories = CategoryService.get_main_categories()
    form.parent_id.choices = [(0, 'None' if lang == 'en' else 'Няма')] + \
        [(c.id, c.get_name(lang)) for c in main_categories]

    if form.validate_on_submit():
        parent_id = form.parent_id.data if form.parent_id.data != 0 else None

        category = CategoryService.create_category(
            name_en=form.name_en.data,
            name_bg=form.name_bg.data,
            description_en=form.description_en.data,
            description_bg=form.description_bg.data,
            parent_id=parent_id,
            icon=form.icon.data,
            image_url=form.image_url.data,
            display_order=form.display_order.data,
            is_active=form.is_active.data
        )

        flash('Category created successfully' if lang ==
              'en' else 'Категорията е създадена успешно', 'success')
        return redirect(url_for('admin.categories'))

    template = f'pages/admin/categories_{lang}.html'
    return render_template(template, form=form, categories=CategoryService.get_all_categories(), edit_mode=False)


@admin_bp.route('/categories/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    lang = session.get('language', 'en')
    category = CategoryService.get_category_by_id(id)

    if not category:
        flash('Category not found' if lang ==
              'en' else 'Категорията не е намерена', 'error')
        return redirect(url_for('admin.categories'))

    form = CategoryForm(obj=category)

    main_categories = [
        c for c in CategoryService.get_main_categories() if c.id != id]
    form.parent_id.choices = [(0, 'None' if lang == 'en' else 'Няма')] + \
        [(c.id, c.get_name(lang)) for c in main_categories]

    if request.method == 'GET':
        form.parent_id.data = category.parent_id if category.parent_id else 0

    if form.validate_on_submit():
        parent_id = form.parent_id.data if form.parent_id.data != 0 else None

        updated_category = CategoryService.update_category(
            category_id=id,
            name_en=form.name_en.data,
            name_bg=form.name_bg.data,
            description_en=form.description_en.data,
            description_bg=form.description_bg.data,
            parent_id=parent_id,
            icon=form.icon.data,
            image_url=form.image_url.data,
            display_order=form.display_order.data,
            is_active=form.is_active.data
        )

        flash('Category updated successfully' if lang ==
              'en' else 'Категорията е обновена успешно', 'success')
        return redirect(url_for('admin.categories'))

    template = f'pages/admin/categories_{lang}.html'
    return render_template(template, form=form, category=category, categories=CategoryService.get_all_categories(), edit_mode=True)


@admin_bp.route('/categories/delete/<int:id>', methods=['POST'])
@login_required
def delete_category(id):
    lang = session.get('language', 'en')

    if CategoryService.delete_category(id):
        flash('Category deleted successfully' if lang ==
              'en' else 'Категорията е изтрита успешно', 'success')
    else:
        flash('Cannot delete category with products or subcategories' if lang ==
              'en' else 'Не може да се изтрие категория с продукти или подкатегории', 'error')

    return redirect(url_for('admin.categories'))


@admin_bp.route('/products')
@login_required
def products():
    lang = session.get('language', 'en')
    page = request.args.get('page', 1, type=int)
    pagination = ProductRepository.get_paginated(page=page, per_page=12)

    template = f'pages/admin/products_{lang}.html'
    return render_template(template, products=pagination.items, pagination=pagination)


@admin_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    lang = session.get('language', 'en')
    form = ProductForm()

    categories = Category.query.filter_by(is_active=True).all()
    form.category_id.choices = [(c.id, c.get_name(lang)) for c in categories]

    if form.validate_on_submit():
        image_url = save_product_image(
            form.image.data) if form.image.data else None
        sku = generate_sku()

        product = Product(
            sku=sku,
            name_en=form.name_en.data,
            name_bg=form.name_bg.data,
            description_en=form.description_en.data,
            description_bg=form.description_bg.data,
            price=form.price.data,
            category_id=form.category_id.data,
            stock=form.stock.data,
            image_url=image_url,
            is_active=form.is_active.data,
            is_featured=form.is_featured.data
        )

        db.session.add(product)
        db.session.commit()

        flash('Product created successfully' if lang ==
              'en' else 'Продуктът е създаден успешно', 'success')
        return redirect(url_for('admin.products'))

    template = f'pages/admin/products_{lang}.html'
    return render_template(template, form=form, products=[], edit_mode=False)


@admin_bp.route('/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    lang = session.get('language', 'en')
    product = ProductRepository.get_by_id(id)

    if not product:
        flash('Product not found' if lang ==
              'en' else 'Продуктът не е намерен', 'error')
        return redirect(url_for('admin.products'))

    form = ProductForm(obj=product)

    categories = Category.query.filter_by(is_active=True).all()
    form.category_id.choices = [(c.id, c.get_name(lang)) for c in categories]

    if form.validate_on_submit():
        if form.image.data:
            if product.image_url:
                delete_product_image(product.image_url)
            product.image_url = save_product_image(form.image.data)

        product.name_en = form.name_en.data
        product.name_bg = form.name_bg.data
        product.description_en = form.description_en.data
        product.description_bg = form.description_bg.data
        product.price = form.price.data
        product.category_id = form.category_id.data
        product.stock = form.stock.data
        product.is_active = form.is_active.data
        product.is_featured = form.is_featured.data

        db.session.commit()

        flash('Product updated successfully' if lang ==
              'en' else 'Продуктът е обновен успешно', 'success')
        return redirect(url_for('admin.products'))

    template = f'pages/admin/products_{lang}.html'
    return render_template(template, form=form, product=product, products=[], edit_mode=True)


@admin_bp.route('/products/delete/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    lang = session.get('language', 'en')
    product = ProductRepository.get_by_id(id)

    if not product:
        flash('Product not found' if lang ==
              'en' else 'Продуктът не е намерен', 'error')
        return redirect(url_for('admin.products'))

    if product.image_url:
        delete_product_image(product.image_url)

    ProductRepository.delete(product)

    flash('Product deleted successfully' if lang ==
          'en' else 'Продуктът е изтрит успешно', 'success')
    return redirect(url_for('admin.products'))


@admin_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    lang = session.get('language', 'en')
    profile_form = UpdateProfileForm(obj=current_user)
    password_form = ChangePasswordForm()

    if 'update_profile' in request.form and profile_form.validate_on_submit():
        if Admin.query.filter(Admin.email == profile_form.email.data, Admin.id != current_user.id).first():
            flash('Email already in use' if lang ==
                  'en' else 'Имейлът вече се използва', 'error')
        else:
            current_user.full_name = profile_form.full_name.data
            current_user.email = profile_form.email.data
            db.session.commit()
            flash('Profile updated successfully' if lang ==
                  'en' else 'Профилът е обновен успешно', 'success')
            return redirect(url_for('admin.profile'))

    if 'change_password' in request.form and password_form.validate_on_submit():
        if not current_user.check_password(password_form.current_password.data):
            flash('Current password is incorrect' if lang ==
                  'en' else 'Текущата парола е грешна', 'error')
        else:
            current_user.set_password(password_form.new_password.data)
            db.session.commit()
            flash('Password changed successfully' if lang ==
                  'en' else 'Паролата е променена успешно', 'success')
            return redirect(url_for('admin.profile'))

    template = f'pages/admin/profile_{lang}.html'
    return render_template(template, profile_form=profile_form, password_form=password_form)
