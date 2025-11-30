# CraftForge Studio - Project Progress Documentation

**Last Updated:** November 30, 2025  
**Current Status:** Stage 2 Complete ✅  
**Development Platforms:** Windows 10/11, Ubuntu Linux  
**Repository:** https://github.com/momchilantonov/CraftForgeStudio

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Complete Project Structure](#complete-project-structure)
3. [Development Stages Overview](#development-stages-overview)
4. [Stage 1: Foundation & Configuration](#stage-1-foundation--configuration)
5. [Stage 2: Public Homepage & Language System](#stage-2-public-homepage--language-system)
6. [Environment Setup (Cross-Platform)](#environment-setup-cross-platform)
7. [Database Schema](#database-schema)
8. [Next Steps: Stage 3](#next-steps-stage-3)
9. [Known Issues & Solutions](#known-issues--solutions)

---

## 🎯 Project Overview

**CraftForge Studio** is a modern bilingual (English/Bulgarian) e-commerce platform built with Flask 3.1.2 and Python 3.12, specializing in 3D-printed models, resin art, plaster creations, and handmade souvenirs.

### Core Features

- **Bilingual Support:** Complete EN/BG translation with session-based language switching
- **Session-Based Shopping:** No user registration required for customers
- **Multiple Payment Methods:** Stripe, PayPal, Cash on Delivery
- **Flexible Delivery:** Home delivery, Econt Office, Econt Box (Bulgarian courier)
- **Admin-Only Management:** Secure admin panel for product/order management
- **Clean Architecture:** Routes → Services → Repositories → Models

### Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Framework | Flask | 3.1.2 |
| Language | Python | 3.12 |
| Database (Dev) | SQLite | 3.x |
| Database (Prod) | PostgreSQL | 15+ |
| ORM | SQLAlchemy | 3.1.1 |
| Migrations | Flask-Migrate | 4.0.7 |
| Authentication | Flask-Login | 0.6.3 |
| Forms | Flask-WTF | 1.2.1 |
| Payments | Stripe | 11.2.0 |
| Frontend | Tailwind CSS | 3.x (CDN) |
| Server (Prod) | Gunicorn | 21.2.0 |

---

## 📁 Complete Project Structure

```
CraftForgeStudio/
├── cfs/                                    # Application root directory
│   ├── app/                                # Main application package
│   │   ├── __init__.py                    # Application factory (create_app)
│   │   ├── config.py                      # Configuration classes (Dev/Prod/Test)
│   │   ├── extensions.py                  # Flask extensions initialization
│   │   │
│   │   ├── models/                        # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   ├── admin.py                   # Admin user model
│   │   │   ├── category.py                # Product category model
│   │   │   ├── order.py                   # Order & OrderItem models
│   │   │   └── product.py                 # Product model
│   │   │
│   │   ├── repositories/                  # Data access layer
│   │   │   ├── __init__.py
│   │   │   ├── base_repository.py         # Base CRUD operations
│   │   │   ├── category_repository.py     # Category queries
│   │   │   ├── order_repository.py        # Order queries
│   │   │   └── product_repository.py      # Product queries
│   │   │
│   │   ├── routes/                        # Flask blueprints (URL routing)
│   │   │   ├── __init__.py                # Blueprint registration
│   │   │   ├── admin.py                   # Admin panel routes
│   │   │   ├── cart.py                    # Shopping cart routes
│   │   │   ├── categories.py              # Category browsing
│   │   │   ├── checkout.py                # Checkout flow
│   │   │   ├── language.py                # Language switching
│   │   │   ├── main.py                    # Homepage & static pages
│   │   │   └── products.py                # Product browsing
│   │   │
│   │   ├── services/                      # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── cart_service.py            # Cart operations
│   │   │   ├── category_service.py        # Category operations
│   │   │   ├── delivery_service.py        # Econt integration
│   │   │   ├── order_service.py           # Order processing
│   │   │   └── payment_service.py         # Payment processing
│   │   │
│   │   ├── forms/                         # WTForms validation
│   │   │   ├── __init__.py
│   │   │   ├── admin_forms.py             # Admin forms
│   │   │   └── checkout_forms.py          # Checkout forms
│   │   │
│   │   ├── templates/                     # Jinja2 HTML templates
│   │   │   ├── base.html                  # Base template structure
│   │   │   │
│   │   │   ├── components/                # Reusable components
│   │   │   │   ├── navbar.html
│   │   │   │   └── footer.html
│   │   │   │
│   │   │   ├── macros/                    # Jinja2 macros
│   │   │   │   └── forms.html
│   │   │   │
│   │   │   ├── errors/                    # Error pages
│   │   │   │   ├── 404_en.html
│   │   │   │   ├── 404_bg.html
│   │   │   │   ├── 500_en.html
│   │   │   │   └── 500_bg.html
│   │   │   │
│   │   │   └── pages/                     # Page templates
│   │   │       ├── home_en.html
│   │   │       ├── home_bg.html
│   │   │       │
│   │   │       ├── admin/                 # Admin templates
│   │   │       │   ├── login_en.html
│   │   │       │   ├── login_bg.html
│   │   │       │   ├── dashboard_en.html
│   │   │       │   ├── dashboard_bg.html
│   │   │       │   ├── categories_en.html
│   │   │       │   ├── categories_bg.html
│   │   │       │   ├── products_en.html
│   │   │       │   ├── products_bg.html
│   │   │       │   ├── orders_en.html
│   │   │       │   └── orders_bg.html
│   │   │       │
│   │   │       ├── cart/                  # Cart templates
│   │   │       │   ├── cart_en.html
│   │   │       │   └── cart_bg.html
│   │   │       │
│   │   │       ├── checkout/              # Checkout templates
│   │   │       │   ├── checkout_en.html
│   │   │       │   ├── checkout_bg.html
│   │   │       │   ├── place_order_en.html
│   │   │       │   ├── place_order_bg.html
│   │   │       │   ├── success_en.html
│   │   │       │   ├── success_bg.html
│   │   │       │   ├── fail_en.html
│   │   │       │   └── fail_bg.html
│   │   │       │
│   │   │       └── products/              # Product templates
│   │   │           ├── category_list_en.html
│   │   │           ├── category_list_bg.html
│   │   │           ├── product_detail_en.html
│   │   │           └── product_detail_bg.html
│   │   │
│   │   ├── static/                        # Static assets
│   │   │   ├── css/
│   │   │   │   └── custom.css
│   │   │   ├── js/
│   │   │   │   ├── cart.js
│   │   │   │   ├── checkout.js
│   │   │   │   └── product.js
│   │   │   └── images/
│   │   │
│   │   └── utils/                         # Utility functions
│   │       ├── __init__.py
│   │       ├── decorators.py              # Custom decorators
│   │       └── helpers.py                 # Helper functions
│   │
│   ├── instance/                          # Local instance folder
│   │   └── craftforge.db                  # SQLite database (dev only)
│   │
│   ├── migrations/                        # Alembic migrations
│   │   ├── versions/
│   │   │   └── 9517da0867ac_initial_migration_models_created.py
│   │   ├── alembic.ini
│   │   ├── env.py
│   │   └── script.py.mako
│   │
│   ├── tests/                             # Test suite
│   │   ├── __init__.py
│   │   ├── unit/
│   │   │   ├── test_cart_service.py
│   │   │   ├── test_order_service.py
│   │   │   └── test_payment_service.py
│   │   └── integration/
│   │
│   ├── run.py                             # Application entry point
│   ├── seed_data.py                       # Database seeding script
│   └── requirements.txt                   # Python dependencies
│
├── development_stages.txt                 # Development roadmap
├── README.md                              # Main documentation
├── README_DEPLOYMENT.md                   # Deployment guide
├── README_PROJECT_SUMMARY.md              # Architecture summary
├── README_PROJECT_PROGRESS.md             # This file
└── LICENSE                                # MIT License
```

---

## 🗓️ Development Stages Overview

The project follows an **11-stage development plan** over 9-13 weeks:

| Stage | Name | Duration | Status |
|-------|------|----------|--------|
| **1** | Foundation & Configuration | 1 week | ✅ Complete |
| **2** | Public Homepage & Language System | 1 week | ✅ Complete |
| **3** | Category & Product Management (Admin) | 1-2 weeks | 🔜 Next |
| **4** | Product Browsing & Search | 1 week | ⏳ Planned |
| **5** | Shopping Cart System | 1 week | ⏳ Planned |
| **6** | Checkout Flow & Order Creation | 1-2 weeks | ⏳ Planned |
| **7** | Econt Delivery Integration | 1 week | ⏳ Planned |
| **8** | Payment Integration (Stripe, PayPal, COD) | 1-2 weeks | ⏳ Planned |
| **9** | Admin Order Management | 1 week | ⏳ Planned |
| **10** | Testing, Refinement & Deployment Prep | 1 week | ⏳ Planned |
| **11** | Production Deployment & Documentation | 1 week | ⏳ Planned |

---

## 🏗️ Stage 1: Foundation & Configuration

**Status:** ✅ Complete  
**Duration:** 1 week  
**Date Completed:** November 29, 2025

### Objectives

Establish project foundation with database models, repository pattern, configuration system, and base templates.

### Components Built

#### 1. Configuration System (`app/config.py`)

**Classes:**
- `Config` - Base configuration with common settings
- `DevelopmentConfig` - SQLite database, debug mode enabled
- `ProductionConfig` - PostgreSQL database, security hardened
- `TestingConfig` - In-memory SQLite, CSRF disabled

**Key Features:**
- Environment-based configuration selection
- Cross-platform database path handling (Windows/Linux)
- Automatic Heroku PostgreSQL URL fix
- Environment variable support for secrets

#### 2. Database Models (`app/models/`)

**Category Model** (`category.py`)
- Fields: id, slug, name_en, name_bg, description_en, description_bg, icon, image_url, is_active, display_order, timestamps
- Methods: `get_name(lang)`, `get_description(lang)`
- Indexes: slug (unique)

**Product Model** (`product.py`)
- Fields: id, sku, name_en, name_bg, description_en, description_bg, price, category_id, stock, image_url, additional_images (JSON), is_active, is_featured, timestamps
- Relationships: Many-to-One with Category
- Properties: `in_stock`
- Methods: `get_name(lang)`, `get_description(lang)`
- Indexes: sku (unique)

**Order Model** (`order.py`)
- Fields: id, order_number, customer info (full_name, email, phone), delivery_method, delivery_address (JSON), payment_method, payment_status, payment_id, subtotal, shipping, total, items (JSON), status, timestamps
- Indexes: order_number (unique)

**OrderItem Model** (`order.py`)
- Fields: id, order_id, product_id, product_name, product_sku, quantity, price, subtotal
- Relationships: Many-to-One with Order, Many-to-One with Product

**Admin Model** (`admin.py`)
- Fields: id, email, password_hash, full_name, is_active, timestamps
- Methods: `set_password()`, `check_password()`, Flask-Login interface methods
- Indexes: email (unique)

**Important:** All models use `datetime.now(timezone.utc)` for Python 3.12 compatibility.

#### 3. Repository Pattern (`app/repositories/`)

**BaseRepository** (`base_repository.py`)
- Methods: `get_by_id()`, `get_all()`, `get_all_active()`, `create()`, `update()`, `delete()`, `save()`

**CategoryRepository** (`category_repository.py`)
- Additional: `get_by_slug()`, `get_all_active_ordered()`, `create_with_slug()`

**ProductRepository** (`product_repository.py`)
- Additional: `get_by_sku()`, `get_by_category()`, `get_featured()`, `search()`, `get_paginated()`

**OrderRepository** (`order_repository.py`)
- Additional: `get_by_order_number()`, `generate_order_number()`, `create_order()`, `get_recent()`, `get_by_status()`

#### 4. Application Factory (`app/__init__.py`)

**Function:** `create_app(config_name=None)`
- Loads environment-based configuration
- Initializes extensions (db, migrate, login_manager)
- Imports all models for migration detection
- Creates instance directory if missing
- Sets default language in session
- Registers blueprints

#### 5. Database Migrations

**Initial Migration:** `9517da0867ac_initial_migration_models_created.py`
- Creates all tables: admin, categories, products, orders, order_items
- Creates indexes on slug, sku, email, order_number

#### 6. Base Templates (`app/templates/`)

**base.html**
- Common HTML structure with DOCTYPE, head, body
- Tailwind CSS CDN integration
- Blocks: title, extra_css, content, extra_js
- Dynamic language attribute from session

**Components:**
- `navbar.html` - Navigation with logo, links, cart icon, language switcher
- `footer.html` - Copyright footer with bilingual text

### Testing Results

- ✅ Database migrations executed successfully
- ✅ All models created in database
- ✅ Repository CRUD operations functional
- ✅ Application starts without errors
- ✅ Templates render correctly
- ✅ Session management working

---

## 🌐 Stage 2: Public Homepage & Language System

**Status:** ✅ Complete  
**Duration:** 1 week  
**Date Completed:** November 30, 2025

### Objectives

Implement bilingual homepage with language switching, featured products display, and category showcase.

### Components Built

#### 1. Blueprint System (`app/routes/`)

**Blueprint Registration** (`__init__.py`)
- Function: `register_blueprints(app)`
- Registers: main_bp, language_bp

**Main Routes** (`main.py`)
- `GET /` - Homepage route
- Fetches language from session (default: 'en')
- Queries featured products (limit 4) and active categories
- Renders language-specific template

**Language Routes** (`language.py`)
- `GET /lang/set/<lang>` - Language switching
- Validates language (en/bg only)
- Sets `session['language']`
- Redirects to referrer or homepage

#### 2. Homepage Templates (`app/templates/pages/`)

**English Homepage** (`home_en.html`)

Sections:
1. Hero - Orange gradient background, title, tagline
2. Featured Products - 4-column grid with product cards
3. Categories - 4-column grid with category boxes
4. About - Description and newsletter form
5. Contact - Contact info and message form

**Bulgarian Homepage** (`home_bg.html`)

Identical structure with Bulgarian translations:
- Hero: "Където технологиите срещат изкуството..."
- Featured: "Препоръчани продукти"
- Categories: "Пазарувай по категории"
- About: "За CraftForge Studio"
- Contact: "Контакти"

#### 3. Updated Components

**Navbar** (`templates/components/navbar.html`)
- Functional language toggle (EN/BG buttons)
- Active language: orange-400 background
- Inactive language: orange-50 background with hover
- Cart icon with hidden badge
- Navigation links with bilingual text

**Footer** (`templates/components/footer.html`)
- Bilingual copyright text
- EN: "All rights reserved."
- BG: "Всички права запазени."

#### 4. Database Seeding (`seed_data.py`)

**Created Data:**
- 4 Categories: 3D Models, Resin Art, Plaster Art, Handmade Souvenirs
- 6 Products: 4 featured (Dragon $29.99, Owl $39.99, Keychain $12.99, Angel $24.99), 2 regular
- 1 Admin User: admin@craftforgestudio.com / admin123

**Features:**
- Clears existing data before seeding
- Visual progress indicators
- Bilingual names and descriptions
- Summary statistics output

#### 5. Design System

**Colors:**
- Background: orange-50 (#FFF7ED)
- Navbar: orange-100 (#FFEDD5)
- Primary buttons: orange-400 (#FB923C)
- Hover: orange-500 (#F97316)
- Text: orange-900 (#7C2D12)

**Layout:**
- Container: max-w-7xl mx-auto px-6
- Grid: grid-cols-1 sm:grid-cols-2 md:grid-cols-4
- Spacing: py-16, py-12, gap-8

**Components:**
- Cards: rounded-lg shadow-md hover:shadow-lg transition
- Buttons: rounded-lg hover:... transition
- Inputs: rounded-lg border-2 border-orange-300

### Testing Results

**Functionality:**
- ✅ Homepage loads at http://localhost:5000
- ✅ 4 featured products display correctly
- ✅ 4 categories display correctly
- ✅ Language switcher changes content
- ✅ Navigation links scroll to sections
- ✅ Cart icon displays (placeholder)

**Language System:**
- ✅ Default language: English
- ✅ BG button switches to Bulgarian
- ✅ EN button switches to English
- ✅ Product/category names translate
- ✅ UI elements translate
- ✅ Session persists language choice

**Visual:**
- ✅ Orange theme consistent
- ✅ Gradient hero section
- ✅ Hover effects working
- ✅ Responsive layout (desktop/tablet/mobile)

---

## ⚙️ Environment Setup (Cross-Platform)

### Prerequisites

- Python 3.12
- Anaconda or Miniconda
- Git
- Text editor (VS Code recommended)

### Setup Instructions

#### 1. Clone Repository

```bash
git clone https://github.com/momchilantonov/CraftForgeStudio.git
cd CraftForgeStudio/cfs
```

#### 2. Create Conda Environment

```bash
conda create -n cfs python=3.12
conda activate cfs
pip install -r requirements.txt
```

#### 3. Configure Environment Variables

**Linux/macOS:** `~/.conda/envs/cfs/etc/conda/activate.d/env_vars.sh`

```bash
#!/bin/bash
export FLASK_APP=run.py
export FLASK_DEBUG=True
export SECRET_KEY='dev-secret-key-change-in-production'
export DATABASE_URL='sqlite:///instance/craftforge.db'
export STRIPE_PUBLIC_KEY='pk_test_your_key'
export STRIPE_SECRET_KEY='sk_test_your_key'
export PAYPAL_CLIENT_ID='your_client_id'
export ADMIN_EMAIL='admin@craftforgestudio.com'
export ADMIN_PASSWORD='admin123'
```

**Deactivation script:** `~/.conda/envs/cfs/etc/conda/deactivate.d/env_vars.sh`

```bash
#!/bin/bash
unset FLASK_APP FLASK_DEBUG SECRET_KEY DATABASE_URL
unset STRIPE_PUBLIC_KEY STRIPE_SECRET_KEY PAYPAL_CLIENT_ID
unset ADMIN_EMAIL ADMIN_PASSWORD
```

Make scripts executable:
```bash
chmod +x ~/.conda/envs/cfs/etc/conda/activate.d/env_vars.sh
chmod +x ~/.conda/envs/cfs/etc/conda/deactivate.d/env_vars.sh
```

**Windows:** `%CONDA_PREFIX%\etc\conda\activate.d\env_vars.ps1`

```powershell
$env:FLASK_APP = "run.py"
$env:FLASK_DEBUG = "True"
$env:SECRET_KEY = "dev-secret-key-change-in-production"
$env:DATABASE_URL = "sqlite:///C:/path/to/CraftForgeStudio/cfs/instance/craftforge.db"
$env:STRIPE_PUBLIC_KEY = "pk_test_your_key"
$env:STRIPE_SECRET_KEY = "sk_test_your_key"
$env:PAYPAL_CLIENT_ID = "your_client_id"
$env:ADMIN_EMAIL = "admin@craftforgestudio.com"
$env:ADMIN_PASSWORD = "admin123"
```

**Note:** Windows requires ABSOLUTE path for DATABASE_URL.

**Deactivation script:** `%CONDA_PREFIX%\etc\conda\deactivate.d\env_vars.ps1`

```powershell
Remove-Item Env:\FLASK_APP -ErrorAction SilentlyContinue
Remove-Item Env:\FLASK_DEBUG -ErrorAction SilentlyContinue
Remove-Item Env:\SECRET_KEY -ErrorAction SilentlyContinue
Remove-Item Env:\DATABASE_URL -ErrorAction SilentlyContinue
Remove-Item Env:\STRIPE_PUBLIC_KEY -ErrorAction SilentlyContinue
Remove-Item Env:\STRIPE_SECRET_KEY -ErrorAction SilentlyContinue
Remove-Item Env:\PAYPAL_CLIENT_ID -ErrorAction SilentlyContinue
Remove-Item Env:\ADMIN_EMAIL -ErrorAction SilentlyContinue
Remove-Item Env:\ADMIN_PASSWORD -ErrorAction SilentlyContinue
```

**Important:** After creating environment variable scripts:
- **Linux/macOS:** Deactivate and reactivate conda environment
- **Windows:** Close PowerShell completely, open new window, then activate conda

#### 4. Initialize Database

```bash
flask db upgrade
python seed_data.py
```

#### 5. Run Application

```bash
python run.py
```

Open browser: http://localhost:5000

### Verification

```bash
# Check environment variables loaded
echo $FLASK_APP          # Linux/macOS
echo $env:FLASK_APP      # Windows

# Verify database exists
ls instance/craftforge.db     # Linux/macOS
dir instance\craftforge.db    # Windows
```

---

## 🗄️ Database Schema

### Entity Relationships

```
categories (1) ──→ (N) products
products (1) ──→ (N) order_items
orders (1) ──→ (N) order_items
admin (standalone - no relationships)
```

### Table Summary

**categories**
- Primary Key: id
- Unique Index: slug
- Bilingual: name_en, name_bg, description_en, description_bg
- Sortable: display_order
- Filterable: is_active

**products**
- Primary Key: id
- Unique Index: sku
- Foreign Key: category_id → categories.id
- Bilingual: name_en, name_bg, description_en, description_bg
- Inventory: stock, is_active
- Features: is_featured (homepage display)
- Media: image_url, additional_images (JSON array)

**orders**
- Primary Key: id
- Unique Index: order_number (format: CFS-YYYYMMDDHHMMSS-HEX)
- Customer: full_name, email, phone
- Delivery: delivery_method (home/office/box), delivery_address (JSON)
- Payment: payment_method (stripe/paypal/cod), payment_status, payment_id
- Pricing: subtotal, shipping, total
- Items: items (JSON snapshot)
- Status: status (pending/confirmed/shipped/delivered/cancelled)

**order_items**
- Primary Key: id
- Foreign Keys: order_id → orders.id, product_id → products.id
- Snapshot: product_name, product_sku (cached at order time)
- Pricing: price, quantity, subtotal

**admin**
- Primary Key: id
- Unique Index: email
- Security: password_hash (Werkzeug)
- Access: is_active

### Current Sample Data

- **Categories:** 4 (3D Models, Resin Art, Plaster Art, Handmade Souvenirs)
- **Products:** 6 (4 featured, 2 regular)
- **Admin Users:** 1 (admin@craftforgestudio.com)
- **Orders:** 0 (created during checkout)

---

## 🚀 Next Steps: Stage 3

**Stage 3: Category & Product Management (Admin)**

**Duration:** 1-2 weeks  
**Status:** 🔜 Next

### Objectives

- Implement admin authentication system
- Create admin dashboard with statistics
- Build category CRUD interface
- Build product CRUD interface with image upload
- Protect admin routes with decorators

### Components to Build

#### 1. Authentication System

**Files:**
- `app/forms/admin_forms.py` - LoginForm
- `app/routes/admin.py` - login, logout, dashboard routes
- `app/templates/pages/admin/login_en.html`
- `app/templates/pages/admin/login_bg.html`

**Features:**
- WTForms with CSRF protection
- Flask-Login session management
- "Remember me" functionality
- `@login_required` decorator

#### 2. Admin Dashboard

**Files:**
- `app/templates/pages/admin/dashboard_en.html`
- `app/templates/pages/admin/dashboard_bg.html`

**Display:**
- Total products, categories, orders count
- Recent orders list (5 most recent)
- Quick action buttons

#### 3. Category Management

**Files:**
- `app/forms/admin_forms.py` - CategoryForm
- `app/routes/admin.py` - category list, add, edit, delete routes
- `app/templates/pages/admin/categories_en.html`
- `app/templates/pages/admin/categories_bg.html`

**Features:**
- List all categories with edit/delete buttons
- Add form: name_en, name_bg, description_en, description_bg, display_order
- Edit form: update existing category
- Delete with confirmation
- Slug auto-generation from English name
- Activate/deactivate toggle

#### 4. Product Management

**Files:**
- `app/forms/admin_forms.py` - ProductForm
- `app/routes/admin.py` - product list, add, edit, delete routes
- `app/templates/pages/admin/products_en.html`
- `app/templates/pages/admin/products_bg.html`
- `app/utils/helpers.py` - Image upload utilities

**Features:**
- List all products with pagination
- Add form: all product fields, category dropdown, image upload
- Edit form: update product, replace image
- Delete with stock check
- SKU auto-generation
- Mark as featured checkbox
- Stock management input

#### 5. Image Upload

**Implementation:**
- File type validation (jpg, png, webp)
- File size limit (5MB max)
- Unique filename generation
- Save to `app/static/images/products/`
- Update product.image_url in database

**New Dependency:**
- Pillow==10.1.0 (for image processing)

### Routes to Implement

```
GET/POST  /admin/login
GET       /admin/logout
GET       /admin/dashboard

GET       /admin/categories
GET/POST  /admin/categories/add
GET/POST  /admin/categories/edit/<id>
POST      /admin/categories/delete/<id>

GET       /admin/products
GET/POST  /admin/products/add
GET/POST  /admin/products/edit/<id>
POST      /admin/products/delete/<id>
```

### Implementation Order

**Week 1:**
1. Days 1-2: Admin authentication (login/logout)
2. Day 3: Admin dashboard
3. Days 4-5: Category CRUD

**Week 2:**
1. Days 1-3: Product CRUD
2. Day 4: Image upload functionality
3. Day 5: Testing and refinement

### Testing Checklist

**Authentication:**
- [ ] Login with valid credentials succeeds
- [ ] Login with invalid credentials fails
- [ ] Logout clears session
- [ ] Protected routes redirect to login
- [ ] "Remember me" persists session

**Category CRUD:**
- [ ] List displays all categories
- [ ] Add creates new category with slug
- [ ] Edit updates category fields
- [ ] Delete removes category (if no products)
- [ ] Display order affects homepage sorting

**Product CRUD:**
- [ ] List displays all products with pagination
- [ ] Add creates product with auto SKU
- [ ] Edit updates product fields
- [ ] Delete removes product
- [ ] Featured products appear on homepage
- [ ] Stock quantity tracked correctly

**Image Upload:**
- [ ] Valid images upload successfully
- [ ] Invalid file types rejected
- [ ] Large files rejected (>5MB)
- [ ] Images display on product page
- [ ] Old images replaced on update

---

## ⚠️ Known Issues & Solutions

### Cross-Platform Issues

#### 1. Database Path Differences

**Issue:** SQLite path handling differs between Windows and Linux

**Solution:**
- **Linux/macOS:** Relative path works: `sqlite:///instance/craftforge.db`
- **Windows:** Requires absolute path: `sqlite:///C:/full/path/to/instance/craftforge.db`
- **Production:** PostgreSQL (no path issues)

**config.py handles this:** Uses `pathlib.Path.as_posix()` for cross-platform compatibility.

#### 2. Conda Environment Variables

**Issue:** Updating activation scripts doesn't reload in current session

**Solution:**
- **Linux/macOS:** `conda deactivate && conda activate cfs`
- **Windows:** Close PowerShell completely, open new window, then `conda activate cfs`

**Why:** Windows PowerShell caches environment variables per session.

#### 3. File Paths in Code

**Issue:** Windows uses backslashes (`\`), Linux uses forward slashes (`/`)

**Solution:** Always use `pathlib.Path` for cross-platform compatibility.

### General Issues

#### 1. Python datetime Deprecation

**Issue:** `datetime.utcnow()` deprecated in Python 3.12

**Solution:** All models use `datetime.now(timezone.utc)`.

#### 2. Flask-Login UserMixin

**Issue:** Admin model must implement Flask-Login interface

**Solution:** Admin model includes required properties: `is_authenticated`, `is_active`, `is_anonymous`, `get_id()`.

#### 3. Import Errors After Changes

**Issue:** Python caches modules in `__pycache__`

**Solution:** Delete cache directories or restart Flask app.

---

## 📚 Quick Reference

### Key Commands

```bash
# Activate environment
conda activate cfs

# Run application
python run.py

# Database migrations
flask db migrate -m "Description"
flask db upgrade
flask db downgrade

# Seed database
python seed_data.py

# Run tests (when implemented)
pytest
pytest --cov=app tests/

# Check environment variables
echo $FLASK_APP          # Linux/macOS
echo $env:FLASK_APP      # Windows
```

### Important URLs

- **Homepage:** http://localhost:5000
- **Language Switch:** http://localhost:5000/lang/set/bg
- **Admin Login:** http://localhost:5000/admin/login (Stage 3)

### Default Credentials

- **Admin Email:** admin@craftforgestudio.com
- **Admin Password:** admin123 (⚠️ change in production)

### File Locations

- **Database:** `cfs/instance/craftforge.db`
- **Migrations:** `cfs/migrations/versions/`
- **Static Files:** `cfs/app/static/`
- **Templates:** `cfs/app/templates/`
- **Environment Config:** `~/.conda/envs/cfs/etc/conda/activate.d/` (Linux) or `%CONDA_PREFIX%\etc\conda\activate.d\` (Windows)

---

## 📝 Development Notes

### Architecture Principles

1. **Separation of Concerns:** Routes → Services → Repositories → Models
2. **No Code Duplication:** Use blueprints, macros, template inheritance
3. **Bilingual First:** Every user-facing text has EN/BG versions
4. **Session-Based:** No user accounts for customers, admin-only authentication
5. **Database-Driven:** Categories and products managed dynamically

### Code Style

- **PEP 8** compliance for Python code
- **Descriptive names** for functions, variables, classes
- **Docstrings** for all public methods
- **Type hints** where helpful
- **Comments** only when logic is complex

### Git Workflow

1. Create feature branch: `git checkout -b feature/name`
2. Make changes and commit: `git commit -m "Description"`
3. Push branch: `git push origin feature/name`
4. Create pull request on GitHub
5. Merge to main after review

### Testing Strategy

- **Unit Tests:** Test individual functions (services, repositories)
- **Integration Tests:** Test complete workflows (checkout, admin CRUD)
- **Manual Testing:** Browser testing for UI/UX
- **Test Data:** Use `seed_data.py` for consistent test data

---

## 🎯 Project Status Summary

**Completed:**
- ✅ Project structure and configuration
- ✅ Database models and migrations
- ✅ Repository pattern implementation
- ✅ Bilingual homepage with language switching
- ✅ Featured products display
- ✅ Category showcase
- ✅ Navigation and footer components
- ✅ Sample data seeding

**In Progress:**
- 🔄 Stage 3: Admin authentication and CRUD

**Upcoming:**
- ⏳ Stage 4: Product browsing and search
- ⏳ Stage 5: Shopping cart
- ⏳ Stage 6-11: Checkout, payments, deployment

---

**Document Version:** 2.0  
**Last Updated:** November 30, 2025  
**Platforms:** Windows 10/11, Ubuntu Linux  
**Ready for:** Stage 3 Development

---

**END OF DOCUMENT**