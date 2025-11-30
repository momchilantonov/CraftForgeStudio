from app import create_app, db
from app.models.category import Category
from app.models.product import Product
from app.models.admin import Admin


def seed_database():
    """Populate database with initial sample data for development and testing."""
    app = create_app('development')

    with app.app_context():
        print("🌱 Starting database seeding...")
        print("=" * 60)

        print("\n🗑️  Clearing existing data...")
        Product.query.delete()
        Category.query.delete()
        Admin.query.delete()
        db.session.commit()
        print("✅ Database cleared")

        print("\n📦 Creating categories...")
        categories_data = [
            {
                'slug': '3d-models',
                'name_en': '3D Models and Files',
                'name_bg': '3D Модели и Файлове',
                'description_en': 'Downloadable 3D printable models and STL files',
                'description_bg': 'Изтегляеми 3D модели за печат и STL файлове',
                'display_order': 1,
                'is_active': True
            },
            {
                'slug': 'resin-art',
                'name_en': 'Resin Art',
                'name_bg': 'Творби от смола',
                'description_en': 'Handcrafted resin sculptures and decorations',
                'description_bg': 'Ръчно изработени смолни скулптури и декорации',
                'display_order': 2,
                'is_active': True
            },
            {
                'slug': 'plaster-art',
                'name_en': 'Plaster Art',
                'name_bg': 'Творби от гипс',
                'description_en': 'Beautiful plaster sculptures and wall art',
                'description_bg': 'Красиви гипсови скулптури и стенни декорации',
                'display_order': 3,
                'is_active': True
            },
            {
                'slug': 'handmade-souvenirs',
                'name_en': 'Handmade Souvenirs',
                'name_bg': 'Ръчно изработени сувенири',
                'description_en': 'Unique handcrafted souvenirs and gifts',
                'description_bg': 'Уникални ръчно изработени сувенири и подаръци',
                'display_order': 4,
                'is_active': True
            }
        ]

        categories = []
        for cat_data in categories_data:
            category = Category(**cat_data)
            db.session.add(category)
            categories.append(category)

        db.session.commit()
        print(f"✅ Created {len(categories)} categories:")
        for cat in categories:
            print(f"   - {cat.get_name('en')} ({cat.slug})")

        print("\n🎨 Creating sample products...")
        products_data = [
            {
                'sku': 'CF-3D-001',
                'name_en': '3D Printed Dragon',
                'name_bg': '3D Принтиран Дракон',
                'description_en': 'High-detail dragon statue, resin-friendly 3D model',
                'description_bg': 'Много детайлен дракон, подходящ за смола',
                'price': 29.99,
                'category_id': categories[0].id,
                'stock': 10,
                'is_active': True,
                'is_featured': True
            },
            {
                'sku': 'CF-RES-001',
                'name_en': 'Resin Owl Sculpture',
                'name_bg': 'Смолна сова',
                'description_en': 'Beautiful resin piece, hand-finished',
                'description_bg': 'Красива смолна фигура, ръчно обработена',
                'price': 39.99,
                'category_id': categories[1].id,
                'stock': 5,
                'is_active': True,
                'is_featured': True
            },
            {
                'sku': 'CF-SOU-001',
                'name_en': 'Handmade Wooden Keychain',
                'name_bg': 'Ръчно изработен дървен ключодържател',
                'description_en': 'Unique wooden keychain with custom engraving',
                'description_bg': 'Уникален дървен ключодържател с персонализирана гравюра',
                'price': 12.99,
                'category_id': categories[3].id,
                'stock': 25,
                'is_active': True,
                'is_featured': True
            },
            {
                'sku': 'CF-PLA-001',
                'name_en': 'Plaster Angel Statue',
                'name_bg': 'Гипсова статуя на ангел',
                'description_en': 'Elegant plaster angel for home decoration',
                'description_bg': 'Елегантен гипсов ангел за домашна декорация',
                'price': 24.99,
                'category_id': categories[2].id,
                'stock': 8,
                'is_active': True,
                'is_featured': True
            },
            {
                'sku': 'CF-3D-002',
                'name_en': 'Fantasy Tower Model',
                'name_bg': 'Фентъзи Кула',
                'description_en': 'Architectural fantasy model for printing',
                'description_bg': 'Архитектурен модел за принтиране',
                'price': 34.99,
                'category_id': categories[0].id,
                'stock': 15,
                'is_active': True,
                'is_featured': False
            },
            {
                'sku': 'CF-RES-002',
                'name_en': 'Ocean Wave Resin Art',
                'name_bg': 'Смолна морска вълна',
                'description_en': 'Ocean-inspired resin art piece',
                'description_bg': 'Вдъхновена от океана смолна творба',
                'price': 45.99,
                'category_id': categories[1].id,
                'stock': 3,
                'is_active': True,
                'is_featured': False
            }
        ]

        for prod_data in products_data:
            product = Product(**prod_data)
            db.session.add(product)

        db.session.commit()
        print(f"✅ Created {len(products_data)} products:")
        for i, prod_data in enumerate(products_data, 1):
            featured = " [FEATURED]" if prod_data['is_featured'] else ""
            print(
                f"   {i}. {prod_data['name_en']} - ${prod_data['price']}{featured}")

        print("\n👤 Creating admin user...")
        admin = Admin(
            email='admin@craftforgestudio.com',
            full_name='Admin User',
            is_active=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created")
        print(f"   Email: admin@craftforgestudio.com")
        print(f"   Password: admin123")
        print("   ⚠️  IMPORTANT: Change password in production!")

        print("\n" + "=" * 60)
        print("🎉 Database seeding completed successfully!")
        print("=" * 60)
        print(f"\n📊 Summary:")
        print(f"   - Categories: {len(categories)}")
        print(f"   - Products: {len(products_data)}")
        print(
            f"   - Featured Products: {sum(1 for p in products_data if p['is_featured'])}")
        print(f"   - Admin Users: 1")
        print("\n✨ Your application is ready for testing!")


if __name__ == '__main__':
    seed_database()
