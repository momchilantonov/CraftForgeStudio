# CraftForge Studio - AI Coding Assistant Guide

### Main task
The main task is to implement the application in production with the structure (architecture) of the project that has already been provided to us. It is ABSOLUTELY FORBIDDEN to change the structure of the project (changing file names, deleting or adding new files, moving directories and files, etc.) without discussing this with the user (me). Some files in the structure do not have code written (the files are empty), but this will change as we progress with the development of the project. The application should be implemented gradually from the basics to more complex logic.

### Follow rules and conventions at all times:
- General Coding Philosophy
    Produce clean, compact, and expressive code with no inline comments; clarity must come from naming and structure.
    Use descriptive names for modules, classes, methods, variables, and template blocks so that comments become unnecessary.
    Prefer short, single-responsibility functions with no side effects and which operate on a consistent abstraction level.
    Start presenting code with public/high-level functions first, followed by internal/implementation details.
    Avoid unnecessary boilerplate or ceremony; do not introduce temporary variables used only once.
    Avoid code repetition and apply inheritance, composition, utility classes, blueprints, macros, and Jinja includes to consolidate variations.
    Keep code testable, deterministic, and structured around pure logic, with side effects isolated.
- Python & Flask Practices
    Structure Flask apps using Blueprints, factories, and a clear separation of concerns (routes, services, repositories, models, forms, etc.).
    Never place business logic inside route handlers; move it to dedicated service classes or functions.
    Keep configuration out of application logic. Use separate config classes and environment-based initialization.
    Favor dataclasses for simple data containers.
    Always validate external inputs and treat request data as untrusted.
    Use WTForms or simple validation layers when appropriate, but keep validation logic centralized.
    Always return clean, structured JSON for API endpoints; do not mix view and API logic.
- Jinja2 Template Practices
    Keep templates minimal: place logic in Python, not the template.
    Favor Jinja macros and template inheritance (base → layout → page) to reduce repetition.
    Use clear and descriptive block names.
    Avoid deeply nested conditionals; compute data in Python before rendering.

- Code Organization & Formatting
    Use consistent, compact formatting with minimal vertical space.
    Do not split method arguments across many lines unless there are more than five.
    Keep modules focused; avoid "god objects" or files with too many responsibilities.
    Prefer returning values instead of mutating external state.
    Ensure all code is easily testable without requiring the full Flask app context unless necessary.
- Testing & Quality
    Write code as if tests will be written for every function; ensure deterministic behavior.
    Favor dependency injection when possible.
    Maintain a clear boundary between pure logic and I/O.
    For data access, wrap database interactions behind repository layers or adapters.
    Before you submit code, make sure it has been tested.
- Security & E-commerce Considerations
    Treat all form data, cookies, and headers as untrusted.
    Apply proper session handling, CSRF protection, password hashing, and safe query practices.
    Never expose sensitive data to templates or logs.
    Keep cart, user, and order logic modular and easily replaceable (e.g., different payment backends).
 - Behavior as an Assistant
    Provide code that is functional, minimal, consistent, and production-ready.
    When asked to build features, propose a clean architecture before writing code.
    If multiple patterns exist, choose the simplest one that keeps the system extensible.
    When offering alternatives, explain trade-offs concisely. Always return all code and all files per task or stage without any other information or explanations, then generate a short and clear review of the work done by going through all changes and new things done.

## Project Overview
Bilingual (EN/BG) Flask 3.1.2 e-commerce platform for 3D models, resin/plaster art. Session-based shopping cart (no user registration), admin-only authentication, clean layered architecture.

**Current Status:** Stage 3 complete (admin panel, category/product CRUD). Stage 4+ (public product browsing, cart, checkout, payments) in progress.

## Architecture

### Layered Design Pattern
**Routes → Services → Repositories → Models**

- **Routes** (`app/routes/*.py`): Flask blueprints handling HTTP, validating forms, rendering templates
- **Services** (`app/services/*.py`): Business logic, data processing, external integrations (mostly empty placeholders for future stages)
- **Repositories** (`app/repositories/*.py`): Data access layer abstracting SQLAlchemy queries
- **Models** (`app/models/*.py`): SQLAlchemy ORM definitions

**Example flow:** `admin.py` route → `CategoryService` → `CategoryRepository` → `Category` model

### Repository Pattern
All repositories extend `BaseRepository` with standard CRUD:
```python
# app/repositories/base_repository.py
get_by_id(id), get_all(), get_all_active(), create(**kwargs), 
update(instance, **kwargs), delete(instance), save(instance)
```
Add model-specific queries in subclasses (e.g., `ProductRepository.search_by_name()`).

### Bilingual System
- **Session-based:** `session['language']` stores `'en'` or `'bg'`, defaults to `'en'`
- **Model fields:** All user-facing text has `_en` and `_bg` columns (e.g., `Category.name_en`, `Category.description_bg`)
- **Templates:** Separate files per language (e.g., `home_en.html`, `home_bg.html`), selected via `f'pages/admin/dashboard_{lang}.html'`
- **Route pattern:** Get `lang = session.get('language', 'en')` → pass to template or call `model.get_name(lang)`

### Database
- **Dev:** SQLite at `instance/craftforge.db` (Windows-compatible path in `config.py` using `Path.as_posix()`)
- **Prod:** PostgreSQL (Heroku-style `postgres://` URLs auto-converted to `postgresql://`)
- **Migrations:** Flask-Migrate (Alembic) in `migrations/versions/`

## Key Conventions

### File Naming
- Templates: `{page}_{lang}.html` (e.g., `login_en.html`, `categories_bg.html`)
- Models: Singular (`category.py`, `product.py`)
- Routes: Plural or feature name (`categories.py`, `checkout.py`)

### Blueprint Registration
Add blueprints in `app/routes/__init__.py`:
```python
def register_blueprints(app):
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
```

### Form Validation
Use Flask-WTF forms from `app/forms/`. CSRF enabled by default (disabled in `TestingConfig` only).

### Admin Routes
Protected with `@login_required` from `flask_login`. Admin model uses `werkzeug.security` for password hashing.

### Static Assets
- Tailwind CSS via CDN in `base.html` (no build process)
- Custom CSS: `app/static/css/custom.css`
- JavaScript placeholders: `cart.js`, `checkout.js`, `product.js` (empty, awaiting Stage 5+)

## Critical Commands

### Environment Setup
```bash
# Create environment
conda create -n cfs python=3.12
conda activate cfs

# Install dependencies
pip install -r requirements.txt
```

### Database Operations
```bash
# Initial setup
flask db init
flask db migrate -m "Description"
flask db upgrade

# Seed test data (clears existing data!)
python cfs/seed_data.py
```

### Running
```bash
# Development server
python cfs/run.py
# Access at http://localhost:5000
```

### Testing
Tests exist in `tests/unit/` but have no implementations yet. Framework: pytest (use `pytest` or `python -m pytest`).

## Development Workflow

### Adding New Features
1. **Model first:** Define SQLAlchemy model with `_en`/`_bg` fields
2. **Migration:** `flask db migrate -m "Description"` → `flask db upgrade`
3. **Repository:** Create/extend repository with query methods
4. **Service:** Add business logic (if complex)
5. **Forms:** Define WTForms in `app/forms/`
6. **Routes:** Create blueprint, use `@login_required` for admin, get `session['language']`
7. **Templates:** Create `{page}_en.html` and `{page}_bg.html`, use `{% extends 'base.html' %}`

### Language Support
When adding UI text:
- Database fields: Add `field_en` and `field_bg` columns
- Model methods: `def get_field(self, lang='en'): return self.field_en if lang == 'en' else self.field_bg`
- Flash messages: `flash('English text' if lang == 'en' else 'Български текст', 'category')`

### File Uploads
Product images go to `app/static/images/products/`. Helper functions in `app/utils/helpers.py`: `save_product_image()`, `delete_product_image()`, `generate_sku()`.

## Integration Points

### Payment Gateways (Stage 8 - not yet implemented)
- Stripe SDK (v14.0.1) via `payment_service.py`
- PayPal REST API
- Cash on Delivery (manual processing)

### Delivery Integration (Stage 7 - not yet implemented)
- Econt API for Bulgarian courier services via `delivery_service.py`

## Configuration

### Environment Variables
Set via Conda activation scripts or `.env`:
```bash
FLASK_APP=run.py
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///instance/craftforge.db
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
ADMIN_EMAIL=admin@craftforgestudio.com
ADMIN_PASSWORD=secure_password
```

### Config Classes
`app/config.py` has `DevelopmentConfig`, `ProductionConfig`, `TestingConfig`. Select via `FLASK_ENV` env var (defaults to `development`).

## Common Pitfalls

1. **Windows paths:** Use `Path.as_posix()` for database URIs (see `config.py`)
2. **Missing language template:** Routes fail if `{page}_{lang}.html` doesn't exist for both `en` and `bg`
3. **Migrations:** Run from project root (`CraftForgeStudio/`), not `cfs/` subdirectory
4. **Session language:** Always check `session.get('language', 'en')` with fallback
5. **Empty services:** `cart_service.py`, `decorators.py` are placeholders - implement before using

## Documentation
- `README.md` - Installation, tech stack, full project structure
- `README_PROJECT_PROGRESS.md` - Stage-by-stage completion status, detailed architecture
- `README_REPOSITORY_FILE_MAP.md` - File tree with GitHub URLs
- `development_stages.txt` - 11-stage roadmap with testing checklist per stage
- `README_DEPLOYMENT.md` - Platform-specific deployment configs (Railway, Render, Heroku)
