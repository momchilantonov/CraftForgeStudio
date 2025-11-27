import os

structure = {
    "cfs": {
        "app": {
            "__init__.py": "",
            "config.py": "",
            "extensions.py": "",

            "models": {
                "__init__.py": "",
                "category.py": "",
                "product.py": "",
                "order.py": "",
                "admin.py": "",
            },

            "repositories": {
                "__init__.py": "",
                "base_repository.py": "",
                "category_repository.py": "",
                "product_repository.py": "",
                "order_repository.py": "",
            },

            "services": {
                "__init__.py": "",
                "category_service.py": "",
                "cart_service.py": "",
                "order_service.py": "",
                "payment_service.py": "",
            },

            "routes": {
                "__init__.py": "",
                "main.py": "",
                "products.py": "",
                "categories.py": "",
                "cart.py": "",
                "checkout.py": "",
                "admin.py": "",
                "language.py": "",
            },

            "forms": {
                "__init__.py": "",
                "checkout_forms.py": "",
                "admin_forms.py": "",
            },

            "utils": {
                "__init__.py": "",
                "decorators.py": "",
                "helpers.py": "",
            },

            "templates": {
                "base.html": "",
                "components": {
                    "navbar.html": "",
                    "footer.html": "",
                },
                "pages": {
                    "home_en.html": "",
                    "home_bg.html": "",
                    "products": {
                        "category_list_en.html": "",
                        "category_list_bg.html": "",
                        "product_detail_en.html": "",
                        "product_detail_bg.html": "",
                    },
                    "cart": {
                        "cart_en.html": "",
                        "cart_bg.html": "",
                    },
                    "checkout": {
                        "checkout_en.html": "",
                        "checkout_bg.html": "",
                        "place_order_en.html": "",
                        "place_order_bg.html": "",
                        "success_en.html": "",
                        "success_bg.html": "",
                        "fail_en.html": "",
                        "fail_bg.html": "",
                    },
                    "admin": {
                        "login_en.html": "",
                        "login_bg.html": "",
                        "dashboard_en.html": "",
                        "dashboard_bg.html": "",
                        "categories_en.html": "",
                        "categories_bg.html": "",
                        "products_en.html": "",
                        "products_bg.html": "",
                        "orders_en.html": "",
                        "orders_bg.html": "",
                    },
                },
                "macros": {
                    "forms.html": "",
                },
                "errors": {
                    "404_en.html": "",
                    "404_bg.html": "",
                    "500_en.html": "",
                    "500_bg.html": "",
                },
            },

            "static": {
                "css": {
                    "custom.css": "",
                },
                "js": {
                    "cart.js": "",
                    "checkout.js": "",
                    "product.js": "",
                },
                "images": {
                    "uploads": {}
                }
            }
        },

        "migrations": {
            ".keep": "",
        },

        "tests": {
            "__init__.py": "",
            "conftest.py": "",
            "unit": {
                "test_cart_service.py": "",
                "test_order_service.py": "",
                "test_payment_service.py": "",
            },
            "integration": {
                "test_checkout_flow.py": "",
                "test_admin_flow.py": "",
            },
        },

        "instance": {
            ".gitignore": "",
        }
    }}


def build(base, tree):
    """Recursively create directories and files"""
    for name, content in tree.items():
        path = os.path.join(base, name)

        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            print(f"Created directory: {path}")
            build(path, content)
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Created file: {path}")


if __name__ == "__main__":
    build("", structure)
    print("\n✔ Nested project structure generated successfully!")
