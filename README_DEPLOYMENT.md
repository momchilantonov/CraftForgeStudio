# Deployment Configuration Templates

This directory contains deployment configuration files for various hosting platforms.

## 📁 Files Overview

| File | Platform | Purpose |
|------|----------|---------|
| `railway.json` | Railway | Railway-specific configuration |
| `nixpacks.toml` | Railway | Build configuration for Railway |
| `render.yaml` | Render | Infrastructure as code for Render |
| `Procfile` | Heroku | Process definitions for Heroku |
| `runtime.txt` | Heroku | Python version specification |
| `pythonanywhere_wsgi.py` | PythonAnywhere | WSGI configuration file |

## 🚀 Quick Start by Platform

### Railway

**Files needed:** `railway.json`, `nixpacks.toml`

1. Copy both files to your project root:
   ```bash
   cp deployment-configs/railway.json .
   cp deployment-configs/nixpacks.toml .
   ```

2. Push to GitHub and connect to Railway
3. Add PostgreSQL database in Railway dashboard
4. Set environment variables in Railway UI
5. Deploy automatically on push

**No additional configuration needed!**

---

### Render

**Files needed:** `render.yaml`

1. Copy to project root:
   ```bash
   cp deployment-configs/render.yaml .
   ```

2. Update values if needed:
   - Change `region` (oregon, frankfurt, singapore)
   - Adjust `plan` (free, starter, standard, pro)

3. Push to GitHub and connect to Render
4. Render reads `render.yaml` automatically
5. Add secret environment variables in Render dashboard

**Database is created automatically!**

---

### Heroku

**Files needed:** `Procfile`, `runtime.txt`

1. Copy both files to project root:
   ```bash
   cp deployment-configs/Procfile .
   cp deployment-configs/runtime.txt .
   ```

2. Install Heroku CLI and login:
   ```bash
   heroku login
   ```

3. Create app and add PostgreSQL:
   ```bash
   heroku create your-app-name
   heroku addons:create heroku-postgresql:mini
   ```

4. Set environment variables:
   ```bash
   heroku config:set FLASK_DEBUG=False
   heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
   # ... add other variables
   ```

5. Deploy:
   ```bash
   git push heroku main
   ```

**Migrations run automatically via `release` command in Procfile!**

---

### PythonAnywhere

**Files needed:** `pythonanywhere_wsgi.py`

1. **Upload your project:**
   ```bash
   # On PythonAnywhere Bash console
   git clone https://github.com/yourusername/craftforge-studio.git
   cd craftforge-studio
   ```

2. **Create virtual environment:**
   ```bash
   mkvirtualenv craftforge --python=python3.12
   pip install -r requirements.txt
   ```

3. **Setup database:**
   - Go to "Databases" tab
   - Initialize PostgreSQL or MySQL
   - Note connection string

4. **Configure WSGI:**
   - Copy `pythonanywhere_wsgi.py` to `/var/www/yourusername_pythonanywhere_com_wsgi.py`
   - Edit the file and update:
     - `USERNAME` (your PythonAnywhere username)
     - `ENV_VARS` (all your environment variables)
     - `DATABASE_URL` (from Databases tab)

5. **Configure Web App:**
   - Go to "Web" tab
   - Set Source code: `/home/yourusername/craftforge-studio`
   - Set Virtualenv: `/home/yourusername/.virtualenvs/craftforge`
   - Set WSGI file: `/var/www/yourusername_pythonanywhere_com_wsgi.py`

6. **Add static files mapping:**
   - URL: `/static/`
   - Directory: `/home/yourusername/craftforge-studio/app/static/`

7. **Initialize database:**
   ```bash
   cd ~/craftforge-studio
   workon craftforge
   flask db upgrade
   python seed_data.py
   ```

8. **Reload web app** (click Reload button)

---

## 🔐 Environment Variables

All platforms require these environment variables:

### Required Variables

```bash
FLASK_DEBUG=False
SECRET_KEY=<generate-with-secrets.token_hex(32)>
DATABASE_URL=<auto-set-by-platform-or-manual>
STRIPE_PUBLIC_KEY=pk_live_your_key
STRIPE_SECRET_KEY=sk_live_your_key
PAYPAL_CLIENT_ID=your_client_id
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=secure_password
```

### How to Generate SECRET_KEY

```python
python -c 'import secrets; print(secrets.token_hex(32))'
```

This generates a secure 64-character hexadecimal string.

---

## 🗄️ Database Configuration

### Railway, Render, Heroku

**DATABASE_URL is set automatically!**

These platforms:
1. Create PostgreSQL database when you add it
2. Set `DATABASE_URL` environment variable automatically
3. Handle SSL connections automatically
4. Provide automatic backups

**You don't need to configure anything manually.**

### PythonAnywhere

**Manual setup required:**

1. Go to "Databases" tab
2. Click "Initialize PostgreSQL" or "Initialize MySQL"
3. Create database:
   ```sql
   CREATE DATABASE craftforge;
   ```
4. Note the connection details
5. Format as `DATABASE_URL`:
   ```
   postgresql://username:password@host/database
   ```
6. Add to WSGI file or environment

---

## 🔄 Automatic Deployments

### Railway & Render

1. Connect GitHub repository
2. Every `git push` triggers automatic deployment
3. Platform runs migrations automatically
4. Zero-downtime deployment (on paid plans)

### Heroku

1. Connect GitHub repository in Heroku dashboard
2. Enable automatic deploys from `main` branch
3. Optionally enable "Wait for CI" to pass tests first
4. Every push triggers deployment

### PythonAnywhere

**Manual deployment:**

```bash
# SSH into PythonAnywhere
cd ~/craftforge-studio
git pull origin main
workon craftforge
pip install -r requirements.txt
flask db upgrade
# Click Reload button in Web tab
```

---

## 🧪 Testing Deployment Locally

Before deploying, test production configuration locally:

### 1. Install Gunicorn

```bash
pip install gunicorn
```

### 2. Set Environment Variables

```bash
export FLASK_DEBUG=False
export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
export DATABASE_URL=sqlite:///instance/craftforge.db
# ... other variables
```

### 3. Run with Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:8000 'app:create_app()'
```

### 4. Test Application

Open http://localhost:8000 and verify:
- [ ] Home page loads
- [ ] Categories work
- [ ] Products display
- [ ] Cart functionality
- [ ] Checkout flow
- [ ] Admin login
- [ ] Language switching

---

## 📊 Platform Comparison

| Feature | Railway | Render | Heroku | PythonAnywhere |
|---------|---------|--------|--------|----------------|
| **Setup Complexity** | ⭐ Easy | ⭐ Easy | ⭐⭐ Medium | ⭐⭐⭐ Complex |
| **Free Tier** | $5 credit | 750 hrs/mo | Eco dynos | Limited |
| **Database Setup** | Automatic | Automatic | Automatic | Manual |
| **Auto Deploy** | Yes | Yes | Yes | No |
| **Custom Domain** | Free | Free | Free | Paid only |
| **Build Time** | Fast | Medium | Medium | N/A |
| **Best For** | Modern apps | Reliability | Enterprise | Learning |

---

## 🆘 Troubleshooting

### Build Fails

**Check:**
- All dependencies in `requirements.txt`
- Python version matches `runtime.txt` or config
- No syntax errors in code

**Solution:**
```bash
# Test locally first
pip install -r requirements.txt
python run.py
```

### Database Connection Error

**Check:**
- `DATABASE_URL` is set correctly
- Database service is running
- Connection string format is correct

**Solution:**
```bash
# Verify DATABASE_URL
echo $DATABASE_URL  # locally
railway variables   # Railway
heroku config       # Heroku
```

### Application Won't Start

**Check:**
- Gunicorn is in `requirements.txt`
- Start command is correct
- Port binding uses `$PORT` variable

**Solution:**
```bash
# Test Gunicorn locally
gunicorn -w 1 -b 0.0.0.0:8000 'app:create_app()'
```

### Migrations Fail

**Check:**
- `flask db upgrade` in build command
- Database is accessible during build
- Migration files are committed to git

**Solution:**
```bash
# Run migrations manually
railway run flask db upgrade  # Railway
heroku run flask db upgrade   # Heroku
```

### Static Files Not Loading

**Check:**
- Static files path is correct in platform settings
- Files are committed to git
- URL mapping is correct

**Solution for PythonAnywhere:**
- Add static files mapping in Web tab:
  - URL: `/static/`
  - Directory: `/home/username/craftforge-studio/app/static/`

---

## 📝 Deployment Checklist

Before deploying to production:

### Code Preparation
- [ ] All code committed and pushed to GitHub
- [ ] All dependencies in `requirements.txt`
- [ ] No sensitive data in code (use environment variables)
- [ ] All tests passing locally
- [ ] `.gitignore` configured correctly

### Platform Configuration
- [ ] Deployment config file added (railway.json, render.yaml, etc.)
- [ ] Python version specified (runtime.txt or config)
- [ ] Start command configured
- [ ] Build command includes migrations

### Environment Variables
- [ ] `FLASK_DEBUG=False`
- [ ] `SECRET_KEY` generated and set
- [ ] Stripe keys (live mode for production)
- [ ] PayPal credentials
- [ ] Admin credentials
- [ ] Database URL (auto-set or manual)

### Database
- [ ] PostgreSQL provisioned
- [ ] Migrations run successfully
- [ ] Seed data loaded
- [ ] Backups enabled (check platform settings)

### Testing
- [ ] Application starts successfully
- [ ] All pages load correctly
- [ ] Checkout flow works end-to-end
- [ ] Payment processing works (test mode first!)
- [ ] Admin panel accessible
- [ ] Language switching works

### Post-Deployment
- [ ] Custom domain configured (if applicable)
- [ ] SSL certificate active (automatic on most platforms)
- [ ] Error monitoring configured (optional)
- [ ] Team notified of deployment
- [ ] Documentation updated

---

## 🔗 Useful Links

### Railway
- Dashboard: https://railway.app
- Documentation: https://docs.railway.app
- CLI: https://docs.railway.app/develop/cli

### Render
- Dashboard: https://dashboard.render.com
- Documentation: https://render.com/docs
- Blueprint Spec: https://render.com/docs/blueprint-spec

### Heroku
- Dashboard: https://dashboard.heroku.com
- Documentation: https://devcenter.heroku.com
- CLI: https://devcenter.heroku.com/articles/heroku-cli

### PythonAnywhere
- Dashboard: https://www.pythonanywhere.com/user/
- Documentation: https://help.pythonanywhere.com
- Flask Guide: https://help.pythonanywhere.com/pages/Flask/

---

**Need help?** Check the main README.md for more detailed deployment instructions.
