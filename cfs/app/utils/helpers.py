import os
import re
import uuid
from werkzeug.utils import secure_filename
from flask import current_app


def generate_slug(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text


def generate_sku(prefix='CF'):
    unique_id = str(uuid.uuid4().hex[:8]).upper()
    return f'{prefix}-{unique_id}'


def save_product_image(image_file):
    if not image_file:
        return None

    filename = secure_filename(image_file.filename)
    unique_filename = f'{uuid.uuid4().hex}_{filename}'

    upload_dir = os.path.join(current_app.root_path,
                              'static', 'images', 'products')
    os.makedirs(upload_dir, exist_ok=True)

    filepath = os.path.join(upload_dir, unique_filename)
    image_file.save(filepath)

    return f'/static/images/products/{unique_filename}'


def delete_product_image(image_url):
    if not image_url or image_url.startswith('http'):
        return

    filepath = os.path.join(current_app.root_path, image_url.lstrip('/'))
    if os.path.exists(filepath):
        os.remove(filepath)
