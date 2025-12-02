# CraftForge Studio - Project Progress Documentation

**Last Updated:** December 2, 2025  
**Current Status:** Stage 3 Complete ✅  
**Development Platforms:** Windows 10/11, Ubuntu Linux  
**Repository:** https://github.com/momchilantonov/CraftForgeStudio

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Complete Project Structure](#complete-project-structure)
3. [Development Stages Overview](#development-stages-overview)
4. [Stage 1: Foundation & Configuration](#stage-1-foundation--configuration)
5. [Stage 2: Public Homepage & Language System](#stage-2-public-homepage--language-system)
6. [Stage 3: Category & Product Management (Admin)](#stage-3-category--product-management-admin)
7. [Environment Setup (Cross-Platform)](#environment-setup-cross-platform)
8. [Database Schema](#database-schema)
9. [Next Steps: Stage 4](#next-steps-stage-4)
10. [Known Issues & Solutions](#known-issues--solutions)

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

Check README_REPOSITORY_FILE_MAP.md

---

## 🗓️ Development Stages Overview

The project follows an **11-stage development plan** over 9-13 weeks:

| Stage | Name | Duration | Status |
|-------|------|----------|--------|
| **1** | Foundation & Configuration | 1 week | ✅ Complete |
| **2** | Public Homepage & Language System | 1 week | ✅ Complete |
| **3** | Category & Product Management (Admin) | 1-2 weeks | ✅ Complete |
| **4** | Product Browsing & Search | 1 week | 🔜 Next |
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
- Fields: id, slug, name_en, name_bg, description_en, description_bg, icon, image_url, parent_id, level, is_active, display_order, timestamps
- **Hierarchical Structure:** Self-referential foreign key for parent-child relationships
  - `parent_id`: References `categories.id` (nullable for main categories)
  - `level`: Integer tracking hierarchy depth (0 = main category, 1+ = subcategories)
- **Relationships:**
  - `parent`: Access parent category (uses `remote_side=[id]`)
  - `subcategories`: Access child categories (backref, lazy='dynamic', ordered by display_order)
  - `products`: One-to-Many with Product (back_populates='category', lazy='dynamic')
- Methods: `get_name(lang)`, `get_description(lang)`, `is_main_category()`, `is_subcategory()`, `get_full_path(lang)`
- Indexes: slug (unique), parent_id

**Product Model** (`product.py`)
- Fields: id, sku, name_en, name_bg, description_en, description_bg, price, category_id, stock, image_url, additional_images (JSON), is_active, is_featured, timestamps
- Relationships: Many-to-One with Category (back_populates='products')
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

## 🛠️ Stage 3: Category & Product Management (Admin)

**Status:** ✅ Complete  
**Duration:** 1-2 weeks  
**Date Completed:** December 2, 2025

### Objectives

Implement complete admin panel with authentication, dashboard, and full CRUD operations for categories and products.

### Components Built

#### 1. Admin Authentication System

**Files:**
- `app/forms/admin_forms.py` - LoginForm, UpdateProfileForm, ChangePasswordForm
- `app/routes/admin.py` - login, logout, dashboard, profile routes
- `app/templates/pages/admin/login_en.html`
- `app/templates/pages/admin/login_bg.html`

**Features:**
- Flask-Login integration with `@login_required` decorator
- WTForms with CSRF protection
- "Remember me" checkbox for persistent sessions
- Account activation status check
- Bilingual error messages
- Next page redirection after login

#### 2. Admin Dashboard

**Files:**
- `app/templates/pages/admin/dashboard_en.html`
- `app/templates/pages/admin/dashboard_bg.html`

**Statistics Display:**
- Total products count
- Total categories count
- Total orders count
- Recent orders list (5 most recent)
- Quick navigation links
- Welcome message with admin name

#### 3. Category Management (Hierarchical)

**Files:**
- `app/services/category_service.py` - Business logic layer
- `app/repositories/category_repository.py` - Enhanced with subcategory methods
- `app/forms/admin_forms.py` - CategoryForm
- `app/templates/pages/admin/categories_en.html`
- `app/templates/pages/admin/categories_bg.html`

**Features:**
- **Hierarchical Structure:** Main categories and subcategories with parent_id/level support
- **CRUD Operations:** Create, read, update, delete with validation
- **Parent Selection:** Dropdown to assign parent category (None for main categories)
- **Slug Auto-generation:** Generated from English name using regex cleanup
- **Display Order:** Sortable field for homepage arrangement
- **Active/Inactive Toggle:** Control category visibility
- **Delete Protection:** Cannot delete categories with products or subcategories
- **Bilingual Forms:** Separate fields for English and Bulgarian

**Category Model Updates:**
- Added `parent_id` foreign key (self-referential)
- Added `level` field (0 = main, 1 = subcategory)
- Added `subcategories` relationship with `back_populates`
- Helper methods: `is_main_category()`, `is_subcategory()`, `get_full_path()`

#### 4. Product Management

**Files:**
- `app/repositories/product_repository.py` - Enhanced with pagination
- `app/forms/admin_forms.py` - ProductForm with FileField
- `app/utils/helpers.py` - Image upload utilities
- `app/templates/pages/admin/products_en.html`
- `app/templates/pages/admin/products_bg.html`

**Features:**
- **CRUD Operations:** Create, read, update, delete products
- **Image Upload:** FileField with validation (jpg, jpeg, png, webp)
- **SKU Auto-generation:** UUID-based unique identifiers (format: CF-XXXXXXXX)
- **Category Dropdown:** Select from active categories with bilingual names
- **Stock Management:** Integer field for inventory tracking
- **Featured Flag:** Checkbox to mark products for homepage display
- **Pagination:** 12 products per page in listing
- **Image Replacement:** Old images deleted when updating with new image
- **Bilingual Forms:** Separate fields for names and descriptions

**Helper Functions:**
- `generate_sku(prefix='CF')` - Creates unique SKU with UUID
- `generate_slug(text)` - Cleans text for URL-safe slugs
- `save_product_image(image_file)` - Validates, saves with unique name to `/static/images/products/`
- `delete_product_image(image_url)` - Removes old images from filesystem

#### 5. Admin Profile Management (Bonus Feature)

**Files:**
- `app/forms/admin_forms.py` - UpdateProfileForm, ChangePasswordForm
- `app/routes/admin.py` - profile route with dual-form handling
- `app/templates/pages/admin/profile_en.html`
- `app/templates/pages/admin/profile_bg.html`

**Features:**
- **Update Profile:** Change full name and email with uniqueness validation
- **Change Password:** Current password verification, minimum 8 characters, confirmation matching
- **Two-Column Layout:** Profile update (left), password change (right)
- **Account Info Display:** Active status, member since date
- **Form Validators:** DataRequired, Email, Length, EqualTo for password confirmation
- **Security:** Email uniqueness check excludes current user

### Implemented Routes

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

GET/POST  /admin/profile
```

### Bilingual Templates

All admin pages created in English and Bulgarian:
- login_en.html / login_bg.html
- dashboard_en.html / dashboard_bg.html
- categories_en.html / categories_bg.html
- products_en.html / products_bg.html
- profile_en.html / profile_bg.html
- orders_en.html / orders_bg.html (empty, for Stage 9)

### New Dependencies

- **Pillow 10.4.0** - Image processing and validation

### Testing Results

**Authentication:**
- ✅ Login with valid credentials succeeds
- ✅ Login with invalid credentials shows error
- ✅ Logout clears session and redirects to homepage
- ✅ Protected routes redirect to login when not authenticated
- ✅ "Remember me" persists session across browser sessions
- ✅ Inactive admin accounts cannot log in

**Category CRUD:**
- ✅ List displays all categories (main and subcategories)
- ✅ Add creates category with auto-generated slug
- ✅ Parent selection dropdown works (None for main categories)
- ✅ Edit updates all category fields correctly
- ✅ Delete removes category (only if no products/subcategories)
- ✅ Display order affects homepage category arrangement
- ✅ Hierarchical relationships maintained (parent_id, level)

**Product CRUD:**
- ✅ List displays products with pagination (12 per page)
- ✅ Add creates product with auto-generated SKU
- ✅ Category dropdown shows only active categories
- ✅ Edit updates all product fields
- ✅ Delete removes product and associated image
- ✅ Featured products appear on homepage
- ✅ Stock quantity updates correctly

**Image Upload:**
- ✅ Valid images (jpg, png, webp) upload successfully
- ✅ Invalid file types rejected with error message
- ✅ Unique filenames generated (UUID-based)
- ✅ Images saved to `/static/images/products/`
- ✅ Old images deleted when product image updated
- ✅ Product display shows uploaded images

**Admin Profile:**
- ✅ Profile form updates full name and email
- ✅ Email uniqueness validated (excluding current user)
- ✅ Password change requires correct current password
- ✅ New password must be minimum 8 characters
- ✅ Password confirmation must match new password
- ✅ Success messages displayed for both operations

---

## 🚀 Next Steps: Stage 4

**Stage 4: Product Browsing & Search (Public)**

**Duration:** 1 week  
**Status:** 🔜 Next

### Objectives

- Create category browsing routes for public users
- Implement product detail pages with full information
- Build product search functionality with filtering
- Add pagination for product listings
- Create breadcrumb navigation

### Components to Build

#### 1. Category Browsing Routes

**Files:**
- `app/routes/categories.py` - Category listing and filtering
- `app/templates/pages/products/category_list_en.html`
- `app/templates/pages/products/category_list_bg.html`

**Features:**
- List all main categories and subcategories
- Filter products by category
- Display product count per category
- Sort products by price, name, newest

#### 2. Product Detail Pages

**Files:**
- `app/routes/products.py` - Product detail view
- `app/templates/pages/products/product_detail_en.html`
- `app/templates/pages/products/product_detail_bg.html`

**Features:**
- Full product information display
- Product image gallery (main + additional_images)
- Add to cart button
- Related products section
- Breadcrumb navigation
- Stock availability indicator

#### 3. Search & Filtering

**Implementation:**
- Search by product name/description
- Filter by category
- Filter by price range
- Filter by availability (in stock)
- Sort options (price, name, newest)

#### 4. Pagination

**Implementation:**
- Products per page: 12
- Page navigation controls
- Total results counter
- "No results" message

### Routes to Implement

```
GET /categories
GET /categories/<slug>
GET /products/<slug>
GET /products/search
```

### Testing Checklist

- [ ] Category listing displays all active categories
- [ ] Products filtered correctly by category
- [ ] Product detail page shows all information
- [ ] Search finds products by name/description
- [ ] Filters work independently and combined
- [ ] Pagination navigates correctly
- [ ] Breadcrumbs show correct path
- [ ] "Add to cart" button appears (functionality in Stage 5)

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
- ✅ Database models and migrations (including hierarchical categories)
- ✅ Repository pattern implementation
- ✅ Bilingual homepage with language switching
- ✅ Featured products display
- ✅ Category showcase
- ✅ Navigation and footer components
- ✅ Sample data seeding
- ✅ Admin authentication system (login, logout, session management)
- ✅ Admin dashboard with statistics
- ✅ Category CRUD with hierarchical support (main/subcategories)
- ✅ Product CRUD with image upload
- ✅ Admin profile management with password change

**In Progress:**
- 🔄 Stage 4: Product browsing and search

**Upcoming:**
- ⏳ Stage 5: Shopping cart system
- ⏳ Stage 6: Checkout flow and order creation
- ⏳ Stage 7-11: Econt delivery, payments, admin orders, testing, deployment

---

**Document Version:** 3.0  
**Last Updated:** December 2, 2025  
**Platforms:** Windows 10/11, Ubuntu Linux  
**Ready for:** Stage 4 Development

---

**END OF DOCUMENT**