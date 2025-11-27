# CraftForge Studio - E-commerce Platform

A modern, multilingual e-commerce platform built with Flask 3.1.2 and Python 3.12, featuring session-based shopping cart, multiple payment methods, and a clean admin panel.

## 🎯 Features

- **Multilingual Support**: Full English/Bulgarian translation
- **Session-Based Cart**: No user registration required
- **Multiple Payment Methods**: Stripe, PayPal, Cash on Delivery
- **Flexible Delivery**: Home delivery, Econt Office, Econt Box
- **Category Management**: Database-driven, admin-manageable categories
- **Admin Panel**: Secure dashboard for managing products, orders, and categories
- **Responsive Design**: Tailwind CSS for mobile-first design
- **Clean Architecture**: Routes → Services → Repositories → Models

## 🏗️ Project Structure

```
app/                                    # Project root
│
├── app/                                # Main application package
│   ├── __init__.py                     # Application factory
│   ├── config.py                       # Environment configurations
│   ├── extensions.py                   # Flask extensions (SQLAlchemy, Migrate, etc.)
│   │
│   ├── models/                         # Database models
│   │   ├── __init__.py
│   │   ├── category.py                 # Category with multilingual fields
│   │   ├── product.py                  # Product with category relationship
│   │   ├── order.py                    # Order with payment/delivery info
│   │   └── admin.py                    # Admin user with Flask-Login
│   │
│   ├── repositories/                   # Data access layer (CRUD operations)
│   │   ├── __init__.py
│   │   ├── base_repository.py          # Base repository with common methods
│   │   ├── category_repository.py      # Category-specific queries
│   │   ├── product_repository.py       # Product queries (search, filter, etc.)
│   │   └── order_repository.py         # Order queries (by status, email, etc.)
│   │
│   ├── services/                       # Business logic layer
│   │   ├── __init__.py
│   │   ├── category_service.py         # Category operations
│   │   ├── cart_service.py             # Cart management (add, update, remove)
│   │   ├── order_service.py            # Order processing
│   │   └── payment_service.py          # Payment gateway integration
│   │
│   ├── routes/                         # Request handlers (blueprints)
│   │   ├── __init__.py
│   │   ├── main.py                     # Home, about, contact
│   │   ├── products.py                 # Product detail, search
│   │   ├── categories.py               # Category listing
│   │   ├── cart.py                     # Cart operations
│   │   ├── checkout.py                 # Checkout flow
│   │   ├── admin.py                    # Admin panel
│   │   └── language.py                 # Language switching
│   │
│   ├── forms/                          # WTForms validation
│   │   ├── __init__.py
│   │   ├── checkout_forms.py           # Checkout and delivery forms
│   │   └── admin_forms.py              # Admin login, category, product forms
│   │
│   ├── utils/                          # Utilities and helpers
│   │   ├── __init__.py
│   │   ├── decorators.py               # @admin_required, @cart_required
│   │   └── helpers.py                  # Format helpers, validators
│   │
│   ├── templates/                      # Jinja2 templates
│   │   ├── base.html                   # Base template
│   │   ├── components/                 # Reusable components
│   │   │   ├── navbar.html
│   │   │   └── footer.html
│   │   ├── pages/                      # Page templates
│   │   │   ├── home_en.html
│   │   │   ├── home_bg.html
│   │   │   ├── products/
│   │   │   │   ├── category_list_en.html
│   │   │   │   ├── category_list_bg.html
│   │   │   │   ├── product_detail_en.html
│   │   │   │   └── product_detail_bg.html
│   │   │   ├── cart/
│   │   │   │   ├── cart_en.html
│   │   │   │   └── cart_bg.html
│   │   │   ├── checkout/
│   │   │   │   ├── checkout_en.html
│   │   │   │   ├── checkout_bg.html
│   │   │   │   ├── place_order_en.html
│   │   │   │   ├── place_order_bg.html
│   │   │   │   ├── success_en.html
│   │   │   │   ├── success_bg.html
│   │   │   │   ├── fail_en.html
│   │   │   │   └── fail_bg.html
│   │   │   └── admin/
│   │   │       ├── login_en.html
│   │   │       ├── login_bg.html
│   │   │       ├── dashboard_en.html
│   │   │       ├── dashboard_bg.html
│   │   │       ├── categories_en.html
│   │   │       ├── categories_bg.html
│   │   │       ├── products_en.html
│   │   │       ├── products_bg.html
│   │   │       ├── orders_en.html
│   │   │       └── orders_bg.html
│   │   ├── macros/
│   │   │   └── forms.html              # Form rendering macros
│   │   └── errors/
│   │       ├── 404_en.html
│   │       ├── 404_bg.html
│   │       ├── 500_en.html
│   │       └── 500_bg.html
│   │
│   └── static/                         # Static assets
│       ├── css/
│       │   └── custom.css              # Custom styles
│       ├── js/
│       │   ├── cart.js                 # Cart interactions
│       │   ├── checkout.js             # Payment/delivery toggles
│       │   └── product.js              # Product gallery, quantity
│       └── images/
│           └── uploads/                # Product images (gitignored)
│
├── migrations/                         # Flask-Migrate database versions
│
├── tests/                              # Test suite
│   ├── __init__.py
│   ├── conftest.py                     # Pytest fixtures
│   ├── unit/                           # Unit tests
│   │   ├── test_cart_service.py
│   │   ├── test_order_service.py
│   │   └── test_payment_service.py
│   └── integration/                    # Integration tests
│       ├── test_checkout_flow.py
│       └── test_admin_flow.py
│
├── instance/                           # Runtime files (gitignored)
│   └── craftforge.db                   # SQLite database
│
├── .gitignore                          # Git ignore rules
├── requirements.txt                    # Production dependencies
├── requirements-dev.txt                # Development dependencies
├── seed_data.py                        # Database seeding script
├── run.py                              # Application entry point
├── LICENSE
└── README.md                           # This file
```

## 🔧 Technology Stack

- **Backend**: Flask 3.1.2, SQLAlchemy, Flask-Migrate
- **Authentication**: Flask-Login (admin only)
- **Forms**: Flask-WTF with CSRF protection
- **Database**: SQLite (development), PostgreSQL (production)
- **Payments**: Stripe 11.2.0, PayPal REST API
- **Frontend**: Tailwind CSS, Vanilla JavaScript
- **Testing**: Pytest, pytest-flask
- **Environment**: Conda

## 🚀 Getting Started

### Prerequisites

- Python 3.12
- Conda (Anaconda or Miniconda)
- Stripe account (for payment testing)
- PayPal developer account (optional)

### Installation

#### 1. Clone the repository

```bash
git clone https://github.com/yourusername/craftforge-studio.git
cd craftforge-studio
```

#### 2. Create and activate Conda environment

```bash
conda create -n cfs python=3.12
conda activate cfs
```

#### 3. Set up environment variables

Create the environment variables script:

```bash
mkdir -p $CONDA_PREFIX/etc/conda/activate.d
nano $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
```

Add the following content:

```bash
#!/bin/bash

# Flask Configuration
export FLASK_APP=run.py
export FLASK_DEBUG=True
export SECRET_KEY='your-secret-key-here-change-in-production'

# Database
export DATABASE_URL='sqlite:///instance/craftforge.db'

# Payment Gateways
export STRIPE_PUBLIC_KEY='pk_test_your_stripe_public_key'
export STRIPE_SECRET_KEY='sk_test_your_stripe_secret_key'
export PAYPAL_CLIENT_ID='your_paypal_client_id'

# Admin Credentials
export ADMIN_EMAIL='admin@craftforgestudio.com'
export ADMIN_PASSWORD='change_this_password'
```

Make it executable:

```bash
chmod +x $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
```

Create deactivation script:

```bash
mkdir -p $CONDA_PREFIX/etc/conda/deactivate.d
nano $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh
```

Add the following content:

```bash
#!/bin/bash

unset FLASK_APP
unset FLASK_DEBUG
unset SECRET_KEY
unset DATABASE_URL
unset STRIPE_PUBLIC_KEY
unset STRIPE_SECRET_KEY
unset PAYPAL_CLIENT_ID
unset ADMIN_EMAIL
unset ADMIN_PASSWORD
```

Make it executable:

```bash
chmod +x $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh
```

Reactivate the environment to load variables:

```bash
conda deactivate
conda activate cfs
```

#### 4. Install dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development/testing
```

#### 5. Initialize the database

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

#### 6. Seed initial data

```bash
python seed_data.py
```

This will create:
- 4 product categories (3D Models, 3D Files, Resin Art, Handmade Souvenirs)
- Sample products in each category
- Admin user (using credentials from environment variables)

#### 7. Run the development server

```bash
python run.py
```

The application will be available at `http://localhost:5000`

## 📦 Dependencies

### Production (`requirements.txt`)

```
Flask==3.1.2
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.7
Flask-Login==0.6.3
Flask-WTF==1.2.1
email-validator==2.2.0
python-dotenv==1.0.1
Werkzeug==3.1.3
stripe==11.2.0
psycopg2-binary==2.9.9
gunicorn==21.2.0
```

**Note:**
- `psycopg2-binary`: PostgreSQL driver (used in production, ignored in local SQLite development)
- `gunicorn`: Production WSGI server (required for deployment)

### Development (`requirements-dev.txt`)

```
pytest==8.3.4
pytest-flask==1.3.0
pytest-cov==6.0.0
```

## 🗄️ Database Schema

### Database Strategy

**Development**: SQLite (simple, zero-config, file-based)
**Production**: PostgreSQL (provided by hosting platform)

**Why this approach?**
- ✅ Easy local development (no database server needed)
- ✅ Production-ready (hosting platforms provide managed PostgreSQL)
- ✅ No code changes between environments
- ✅ SQLAlchemy ORM handles both databases transparently

### Development Database (SQLite)

SQLite is perfect for local development:

```bash
# In conda activate.d/env_vars.sh
export DATABASE_URL='sqlite:///instance/craftforge.db'
```

**Features:**
- Single file database (`instance/craftforge.db`)
- No server installation required
- Fast for development and testing
- Easy to reset (just delete the file)
- Automatically created when app first runs

### Production Database (PostgreSQL)

Hosting platforms automatically provide managed PostgreSQL databases:

| Platform | Database | Auto-Provisioned | Backup | SSL |
|----------|----------|------------------|--------|-----|
| Railway | PostgreSQL 15+ | ✅ Yes | ✅ Yes | ✅ Yes |
| Render | PostgreSQL 14+ | ✅ Yes | ✅ Yes | ✅ Yes |
| Heroku | PostgreSQL 15 | ✅ Yes (addon) | ✅ Yes | ✅ Yes |
| PythonAnywhere | MySQL/PostgreSQL | ⚠️ Manual setup | ✅ Yes | ✅ Yes |

**The platform sets `DATABASE_URL` automatically:**
```
postgresql://user:password@host:5432/database_name
```

**You never need to manually configure the production database!**

### Schema Tables

### Categories Table

```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    slug VARCHAR(50) UNIQUE NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    name_bg VARCHAR(100) NOT NULL,
    description_en TEXT,
    description_bg TEXT,
    icon VARCHAR(50),
    image_url VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Products Table

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    name_en VARCHAR(200) NOT NULL,
    name_bg VARCHAR(200) NOT NULL,
    description_en TEXT,
    description_bg TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category_id INTEGER NOT NULL,
    stock INTEGER DEFAULT 0,
    image_url VARCHAR(255),
    additional_images JSON,
    is_active BOOLEAN DEFAULT TRUE,
    is_featured BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
```

### Orders Table

```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    delivery_method VARCHAR(20) NOT NULL,
    delivery_address JSON NOT NULL,
    payment_method VARCHAR(20) NOT NULL,
    payment_status VARCHAR(20) DEFAULT 'pending',
    payment_id VARCHAR(100),
    subtotal DECIMAL(10, 2) NOT NULL,
    shipping DECIMAL(10, 2) NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    items JSON NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Admin Table

```sql
CREATE TABLE admin (
    id INTEGER PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🛣️ URL Structure

### Public Routes

| URL | Method | Description |
|-----|--------|-------------|
| `/` | GET | Home page |
| `/lang/set/<lang>` | GET | Set language (en/bg) |
| `/categories/<slug>` | GET | Category products |
| `/products/<id>` | GET | Product detail |
| `/products/search` | GET | Search products |
| `/cart` | GET | View cart |
| `/cart/add` | POST | Add to cart |
| `/cart/update` | POST | Update quantity |
| `/cart/remove` | POST | Remove item |
| `/checkout` | GET, POST | Checkout form |
| `/checkout/place-order` | GET, POST | Review order |
| `/checkout/finalize-order` | POST | Process payment |
| `/checkout/success/<order_number>` | GET | Payment success |
| `/checkout/failed` | GET | Payment failed |

### Admin Routes

| URL | Method | Description |
|-----|--------|-------------|
| `/admin/login` | GET, POST | Admin login |
| `/admin/logout` | GET | Admin logout |
| `/admin/dashboard` | GET | Admin dashboard |
| `/admin/categories` | GET, POST | Manage categories |
| `/admin/products` | GET, POST | Manage products |
| `/admin/orders` | GET | Manage orders |

## 🔐 Security Features

- **CSRF Protection**: All forms protected with Flask-WTF
- **Password Hashing**: Werkzeug security for admin passwords
- **Session Security**: Secure session cookies
- **Input Validation**: WTForms validation on all user inputs
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection
- **XSS Protection**: Jinja2 auto-escaping

## 🌍 Multilingual Support

### How it Works

1. **Session-Based**: Language preference stored in `session['language']`
2. **Dual Fields**: Models have `name_en`, `name_bg`, `description_en`, `description_bg`
3. **Separate Templates**: Each page has `_en.html` and `_bg.html` versions
4. **Helper Methods**: Models provide `get_name(lang)`, `get_description(lang)`

### Language Toggle

```html
<!-- Language switcher in navbar -->
<div class="flex rounded-full overflow-hidden border-2 border-orange-400">
  <a href="{{ url_for('language.set_language', lang='en') }}"
     class="w-7 h-7 bg-orange-400 text-white">EN</a>
  <a href="{{ url_for('language.set_language', lang='bg') }}"
     class="w-7 h-7 bg-orange-50 text-orange-900">BG</a>
</div>
```

## 💳 Payment Integration

### Supported Methods

1. **Cash on Delivery (COD)**
   - Immediate order confirmation
   - No payment gateway required
   - Status: `payment_confirmed`

2. **Stripe**
   - Redirect to Stripe Checkout
   - Webhook for payment confirmation
   - Test mode keys in development

3. **PayPal**
   - PayPal REST API integration
   - Client-side button rendering
   - Sandbox mode for testing

### Payment Flow

```
Cart → Checkout Form → Review Order → Payment Gateway → Success/Failure
```

### Implementation Notes

- Stock reduced only after successful payment
- Cart cleared only on payment success
- Order status tracked: `pending` → `confirmed` / `payment_failed`
- Payment ID stored for reference and refunds

## 🛒 Shopping Cart

### Cart Structure (Session)

```python
session['cart'] = {
    'items': [
        {
            'product_id': 1,
            'name': 'Dragon Statue',
            'price': 29.99,
            'quantity': 2,
            'image_url': '/static/images/products/dragon.jpg'
        }
    ],
    'subtotal': 59.98,
    'shipping': 5.00,
    'total': 64.98
}
```

### Cart Operations

- `add_item(product_id, quantity)`: Add product or update quantity
- `update_quantity(product_id, quantity)`: Change item quantity
- `remove_item(product_id)`: Remove item from cart
- `calculate_totals()`: Recalculate subtotal, shipping, total
- `validate_cart()`: Check stock availability
- `clear_cart()`: Empty cart after successful order

## 🧪 Testing

### Run all tests

```bash
pytest
```

### Run with coverage

```bash
pytest --cov=app tests/
```

### Run specific test file

```bash
pytest tests/unit/test_cart_service.py
```

### Test Structure

- **Unit Tests**: Test individual services (cart, order, payment)
- **Integration Tests**: Test complete flows (checkout, admin operations)
- **Fixtures**: `conftest.py` provides app, client, database fixtures

## 📝 Development Workflow

### 1. Create a new feature branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make changes following the architecture

- **Models**: Add/modify in `app/models/`
- **Repositories**: Database operations in `app/repositories/`
- **Services**: Business logic in `app/services/`
- **Routes**: HTTP handlers in `app/routes/`
- **Templates**: Jinja2 templates in `app/templates/`

### 3. Run tests

```bash
pytest
```

### 4. Commit and push

```bash
git add .
git commit -m "Add feature: description"
git push origin feature/your-feature-name
```

### 5. Create pull request

## 🎨 Customization

### Adding a New Category

1. Use admin panel at `/admin/categories`
2. Or use `seed_data.py` script:

```python
from app.repositories.category_repository import CategoryRepository

repo = CategoryRepository()
repo.create_with_slug(
    slug='new-category',
    name_en='New Category',
    name_bg='Нова Категория',
    description_en='Description',
    description_bg='Описание'
)
```

### Adding a New Payment Method

1. Add method to `app/services/payment_service.py`
2. Update `CheckoutForm` in `app/forms/checkout_forms.py`
3. Add handler in `app/routes/checkout.py`
4. Update checkout templates

## 🚢 Deployment

### Platform Comparison

| Feature | Railway | Render | Heroku | PythonAnywhere |
|---------|---------|--------|--------|----------------|
| **Free Tier** | $5 credit/month | 750 hrs/month | Eco dynos | Limited free |
| **Database** | PostgreSQL (auto) | PostgreSQL (auto) | PostgreSQL (addon) | Manual setup |
| **Setup Time** | < 5 minutes | < 5 minutes | < 10 minutes | ~30 minutes |
| **GitHub Deploy** | ✅ Auto | ✅ Auto | ✅ Auto | ❌ Manual |
| **Custom Domain** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes (paid) |
| **SSL Certificate** | ✅ Auto | ✅ Auto | ✅ Auto | ✅ Auto (paid) |
| **Best For** | Modern apps | Modern apps | Enterprise | Beginners |

**Recommendation:** Railway or Render for easiest deployment.

---

### 🚂 Railway Deployment

**Why Railway:**
- Simplest deployment process
- Automatic PostgreSQL provisioning
- GitHub integration with auto-deploys
- Generous free tier
- Great for Flask apps

#### Step 1: Create `railway.json`

Create this file in your project root:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn -w 4 -b 0.0.0.0:$PORT 'app:create_app()'",
    "healthcheckPath": "/",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### Step 2: Create `nixpacks.toml`

```toml
[phases.setup]
nixPkgs = ["python312"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[phases.build]
cmds = ["flask db upgrade"]

[start]
cmd = "gunicorn -w 4 -b 0.0.0.0:$PORT 'app:create_app()'"
```

#### Step 3: Deploy

1. **Push code to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for Railway deployment"
   git push origin main
   ```

2. **Go to [railway.app](https://railway.app)**
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Add PostgreSQL Database:**
   - Click "+ New" → "Database" → "Add PostgreSQL"
   - Railway automatically sets `DATABASE_URL`

4. **Set Environment Variables:**

   In Railway dashboard, add these variables:
   ```
   FLASK_DEBUG=False
   SECRET_KEY=<generate-with-python-secrets.token_hex(32)>
   STRIPE_PUBLIC_KEY=pk_live_your_key
   STRIPE_SECRET_KEY=sk_live_your_key
   PAYPAL_CLIENT_ID=your_paypal_client_id
   ADMIN_EMAIL=admin@craftforgestudio.com
   ADMIN_PASSWORD=<secure-password>
   ```

5. **Deploy!**
   - Railway automatically deploys on git push
   - View logs in real-time
   - Get your app URL: `yourapp.railway.app`

6. **Seed Production Data:**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli

   # Login and link project
   railway login
   railway link

   # Run seed script
   railway run python seed_data.py
   ```

---

### 🎨 Render Deployment

**Why Render:**
- Simple and reliable
- Automatic HTTPS
- Free tier with PostgreSQL
- Zero-downtime deploys

#### Step 1: Create `render.yaml`

Create this file in your project root:

```yaml
services:
  - type: web
    name: craftforge-studio
    env: python
    region: frankfurt  # or oregon, singapore
    plan: free
    buildCommand: "pip install -r requirements.txt && flask db upgrade"
    startCommand: "gunicorn -w 4 -b 0.0.0.0:$PORT 'app:create_app()'"
    envVars:
      - key: FLASK_DEBUG
        value: False
      - key: SECRET_KEY
        generateValue: true
      - key: PYTHON_VERSION
        value: 3.12.0
      - key: DATABASE_URL
        fromDatabase:
          name: craftforge-db
          property: connectionString
      - key: STRIPE_PUBLIC_KEY
        sync: false
      - key: STRIPE_SECRET_KEY
        sync: false
      - key: PAYPAL_CLIENT_ID
        sync: false
      - key: ADMIN_EMAIL
        sync: false
      - key: ADMIN_PASSWORD
        sync: false

databases:
  - name: craftforge-db
    databaseName: craftforge
    plan: free
    region: frankfurt
```

#### Step 2: Deploy

1. **Push code to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Go to [render.com](https://render.com)**
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Render detects `render.yaml` automatically

3. **Set Secret Environment Variables:**

   In Render dashboard, add values for:
   ```
   STRIPE_PUBLIC_KEY
   STRIPE_SECRET_KEY
   PAYPAL_CLIENT_ID
   ADMIN_EMAIL
   ADMIN_PASSWORD
   ```

4. **Deploy!**
   - Render creates both web service and PostgreSQL database
   - Automatic HTTPS with custom domain support
   - Get your URL: `yourapp.onrender.com`

5. **Seed Production Data:**
   ```bash
   # Use Render Shell from dashboard
   # Or use Render CLI
   python seed_data.py
   ```

---

### 🟣 Heroku Deployment

**Why Heroku:**
- Industry standard
- Extensive addon marketplace
- Great documentation
- Enterprise-ready

#### Step 1: Create `Procfile`

Create this file in your project root:

```
web: gunicorn -w 4 -b 0.0.0.0:$PORT 'app:create_app()'
release: flask db upgrade
```

#### Step 2: Create `runtime.txt`

```
python-3.12.0
```

#### Step 3: Deploy

1. **Install Heroku CLI:**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku

   # Ubuntu/Debian
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login and Create App:**
   ```bash
   heroku login
   heroku create craftforge-studio
   ```

3. **Add PostgreSQL:**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

   This automatically sets `DATABASE_URL`.

4. **Set Environment Variables:**
   ```bash
   heroku config:set FLASK_DEBUG=False
   heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
   heroku config:set STRIPE_PUBLIC_KEY=pk_live_your_key
   heroku config:set STRIPE_SECRET_KEY=sk_live_your_key
   heroku config:set PAYPAL_CLIENT_ID=your_paypal_client_id
   heroku config:set ADMIN_EMAIL=admin@craftforgestudio.com
   heroku config:set ADMIN_PASSWORD=secure_password
   ```

5. **Deploy:**
   ```bash
   git push heroku main
   ```

   Heroku automatically:
   - Detects Python app
   - Installs dependencies
   - Runs migrations (via `release` in Procfile)
   - Starts the app

6. **Seed Production Data:**
   ```bash
   heroku run python seed_data.py
   ```

7. **Open App:**
   ```bash
   heroku open
   ```

---

### 🐍 PythonAnywhere Deployment

**Why PythonAnywhere:**
- Beginner-friendly
- Free tier available
- Good for learning
- SSH access included

**Note:** PythonAnywhere requires more manual setup.

#### Step 1: Upload Code

1. **Create account at [pythonanywhere.com](https://pythonanywhere.com)**

2. **Open Bash console and clone repo:**
   ```bash
   git clone https://github.com/yourusername/craftforge-studio.git
   cd craftforge-studio
   ```

3. **Create virtual environment:**
   ```bash
   mkvirtualenv craftforge --python=python3.12
   pip install -r requirements.txt
   ```

#### Step 2: Setup Database

1. **Go to "Databases" tab**
   - Initialize PostgreSQL or MySQL
   - Note the connection details

2. **Set DATABASE_URL:**
   ```bash
   # In .bashrc or in WSGI file
   export DATABASE_URL='postgresql://user:pass@host/dbname'
   # or
   export DATABASE_URL='mysql://user:pass@host/dbname'
   ```

#### Step 3: Configure WSGI

Create `/var/www/yourusername_pythonanywhere_com_wsgi.py`:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/craftforge-studio'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment variables
os.environ['FLASK_DEBUG'] = 'False'
os.environ['SECRET_KEY'] = 'your-secret-key'
os.environ['DATABASE_URL'] = 'your-database-url'
os.environ['STRIPE_PUBLIC_KEY'] = 'pk_live_your_key'
os.environ['STRIPE_SECRET_KEY'] = 'sk_live_your_key'
os.environ['PAYPAL_CLIENT_ID'] = 'your_client_id'
os.environ['ADMIN_EMAIL'] = 'admin@craftforgestudio.com'
os.environ['ADMIN_PASSWORD'] = 'secure_password'

# Import Flask app
from app import create_app
application = create_app()
```

#### Step 4: Configure Web App

1. **Go to "Web" tab**
   - Click "Add a new web app"
   - Choose "Manual configuration"
   - Select Python 3.12

2. **Set paths:**
   - Source code: `/home/yourusername/craftforge-studio`
   - Working directory: `/home/yourusername/craftforge-studio`
   - WSGI file: `/var/www/yourusername_pythonanywhere_com_wsgi.py`

3. **Set virtualenv:**
   ```
   /home/yourusername/.virtualenvs/craftforge
   ```

4. **Add static files mapping:**
   - URL: `/static/`
   - Directory: `/home/yourusername/craftforge-studio/app/static/`

#### Step 5: Initialize Database

```bash
cd ~/craftforge-studio
workon craftforge
flask db upgrade
python seed_data.py
```

#### Step 6: Reload Web App

Click "Reload" button in Web tab.

---

### 🔒 Production Checklist

Before deploying to production, ensure:

**Security:**
- [ ] `FLASK_DEBUG=False` (critical!)
- [ ] Generate secure `SECRET_KEY`: `python -c 'import secrets; print(secrets.token_hex(32))'`
- [ ] Use environment variables for all secrets
- [ ] Enable HTTPS (automatic on most platforms)
- [ ] Use Stripe live keys (not test keys)
- [ ] Change default admin password

**Database:**
- [ ] PostgreSQL configured (automatic on Railway/Render/Heroku)
- [ ] Migrations run: `flask db upgrade`
- [ ] Database backups enabled (automatic on managed platforms)

**Application:**
- [ ] All dependencies in `requirements.txt`
- [ ] Gunicorn configured as WSGI server
- [ ] Static files served correctly
- [ ] Error logging configured

**Testing:**
- [ ] All tests passing: `pytest`
- [ ] Test checkout flow manually
- [ ] Test payment methods (Stripe test mode first)
- [ ] Test admin panel access
- [ ] Test multilingual switching

**Post-Deployment:**
- [ ] Run seed script: `python seed_data.py`
- [ ] Test live site thoroughly
- [ ] Set up custom domain (if needed)
- [ ] Configure monitoring/alerts
- [ ] Document deployment process for team

---

### 🔄 Continuous Deployment

All platforms support automatic deployment on git push:

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Update feature"
   git push origin main
   ```

2. **Platform automatically:**
   - Detects changes
   - Runs tests (if configured)
   - Builds application
   - Runs migrations
   - Deploys new version
   - Zero downtime (on paid tiers)

---

### 📊 Environment Variables Reference

**Required in Production:**

| Variable | Example | Description |
|----------|---------|-------------|
| `FLASK_DEBUG` | `False` | Must be False in production |
| `SECRET_KEY` | `<64-char-hex>` | Generate with secrets.token_hex(32) |
| `DATABASE_URL` | `postgresql://...` | Auto-set by platform |
| `STRIPE_PUBLIC_KEY` | `pk_live_...` | Stripe publishable key |
| `STRIPE_SECRET_KEY` | `sk_live_...` | Stripe secret key |
| `PAYPAL_CLIENT_ID` | `<client-id>` | PayPal REST API client |
| `ADMIN_EMAIL` | `admin@example.com` | Admin login email |
| `ADMIN_PASSWORD` | `<secure-pass>` | Admin login password |

**Optional:**

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | Platform-set | Port to bind to (auto-set) |
| `WEB_CONCURRENCY` | `4` | Number of Gunicorn workers |
| `MAX_CONTENT_LENGTH` | `16777216` | Max upload size (16MB) |

---

### 🆘 Troubleshooting Deployment

**App won't start:**
```bash
# Check logs
railway logs           # Railway
heroku logs --tail     # Heroku
# Render: View logs in dashboard
```

**Database connection fails:**
```bash
# Verify DATABASE_URL is set
railway variables      # Railway
heroku config          # Heroku
```

**Migrations fail:**
```bash
# Run migrations manually
railway run flask db upgrade
heroku run flask db upgrade
```

**Static files not loading:**
- Check static files mapping in platform settings
- Verify `app/static/` path is correct
- Ensure WhiteNoise is configured (some platforms)

**Import errors:**
```bash
# Verify all dependencies in requirements.txt
# Check Python version matches runtime.txt
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For issues and questions:
- Create an issue on GitHub
- Email: support@craftforgestudio.com

## 🙏 Acknowledgments

- Flask documentation and community
- Tailwind CSS for the design system
- Stripe and PayPal for payment processing
- All contributors and supporters

---

**Built with ❤️ using Flask and Python**
