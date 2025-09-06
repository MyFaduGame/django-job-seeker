# JobPortal — README

**A detailed, step-by-step guide to the Django admin panel and HTML pages** for the JobPortal project (accounts + jobs apps). This README documents setup, admin usage, templates, styling and next steps.

---

## Table of Contents

1. Project overview
2. Prerequisites
3. Quick start (setup & run locally)
4. Project structure
5. Important settings changes
6. Database & environment configuration (recommended)
7. Models overview (what each model contains)
8. Django Admin — step-by-step usage & features
9. Accounts (auth) — views, templates & flows
10. Employers — dashboard & job management flow
11. Job Seekers — search, view, apply flows
12. Forms, file uploads & validation
13. Signals (auto-create profiles)
14. Templates & static files (how to organize; theme)
15. Media handling & production storage (S3 suggestion)
16. Security checklist & best practices
17. Deployment notes (gunicorn, nginx, collectstatic, Docker)
18. Tests, migrations and fixtures
19. Troubleshooting common errors
20. Useful commands summary
21. Extending the project (next features)
22. License & contribution

---

## 1. Project overview

This Django app consists of two main apps:

* `accounts`: custom `User` model (with `role`) and `EmployerProfile`.
* `jobs`: job `Category`, `Job`, and `Application` models.

Primary user roles and features:

* **Admin** : manage users, employers, jobs and applications via Django admin with custom actions (verify employer, deactivate jobs, export applicant CSV).
* **Employers** : register, create `EmployerProfile`, post and manage jobs, view applications.
* **Job Seekers** : register, search jobs (filters), view details, upload resume & apply.

The repo includes styled HTML pages (neon/coder theme) for auth, job listing, job detail, application forms.

---

## 2. Prerequisites

* Python 3.10+ (3.11 recommended)
* pip
* PostgreSQL (recommended for production) or SQLite (dev)
* Git
* (Optional) Docker & Docker Compose

---

## 3. Quick start (setup & run locally)

```bash
# clone
git clone https://github.com/MyFaduGame/django-job-seeker.git
cd jobportal

# create venv
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.\.venv\Scripts\activate  # Windows (PowerShell)

# install
pip install -r requirements.txt

# set environment variables (see section 6 for details)
# e.g. create a .env file with SECRET_KEY and DB creds

# make migrations & migrate
python manage.py makemigrations
python manage.py migrate

# create superuser
python manage.py createsuperuser

# run
python manage.py runserver
```

Visit `http://127.0.0.1:8000/admin/` for the admin panel and `http://127.0.0.1:8000/` for the site.

---

## 4. Project structure (recommended layout)

```
jobportal/
├─ jobportal/            # project settings
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
├─ accounts/             # users, employer profile
│  ├─ models.py
│  ├─ forms.py
│  ├─ views.py
│  ├─ urls.py
│  ├─ admin.py
│  └─ signals.py
├─ jobs/
│  ├─ models.py
│  ├─ forms.py
│  ├─ views.py
│  ├─ urls.py
│  └─ admin.py
├─ templates/
│  ├─ accounts/
│  ├─ jobs/
│  └─ base.html
├─ static/
│  ├─ css/
│  └─ js/
├─ media/
└─ manage.py
```

---

## 5. Important settings changes

Make sure your `settings.py` includes the following key config:

```py
# custom user
AUTH_USER_MODEL = 'accounts.User'

# templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {...}
    }
]

# media
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# static
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

**Environment variables** (don't commit `.env`):

```
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgres://user:pass@host:5432/jobportal
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## 6. Database & environment configuration (recommended)

 **Development** : `SQLite` works out of the box (no config required). For production use `Postgres`. Use `django-environ` or `psycopg2` with an env var `DATABASE_URL`.

Example `DATABASES` using `django-environ`:

```py
import environ
env = environ.Env()
DATABASES = {'default': env.db('DATABASE_URL')}
```

---

## 7. Models overview

**accounts.User** (custom `AbstractUser`)

* `role` (`admin` / `employer` / `jobseeker`)
* `phone` etc.

**accounts.EmployerProfile**

* `user` (OneToOne)
* `company_name`, `website`, `location`, `logo`, `description`, `verified` etc.

**jobs.Category** (optional)

* `name`

**jobs.Job**

* `title`, `company`(FK to EmployerProfile), `location`, `category`, `description`, `salary_min`, `salary_max`, `employment_type`, `is_active`, `posted_at`, `expires_at`, `slug`

**jobs.Application**

* `job` (FK), `applicant` (FK to User), `resume` (FileField), `cover_letter`, `applied_at`, `status`

---

## 8. Django Admin — step-by-step usage & features

### Access the admin panel

1. Create a superuser:

```bash
python manage.py createsuperuser
```

2. Visit: `http://127.0.0.1:8000/admin/`

### Useful admin features implemented

* **User admin** : list & filter users by role, edit extra fields (`role`, `phone`).
* **EmployerProfile admin** : fields: `company_name`, `user`, `location`, `verified`. Has a bulk action `verify_employers` to mark selected employers as verified.
* **Job admin** : inline `Application`s, actions: `deactivate_jobs`, `export_applicants_csv`.
* **Application admin** : view applicants, filter by status.

### How to use the `verify_employers` action

1. Navigate to Employers in admin.
2. Select the companies you want to approve.
3. Choose **"Mark selected employers as verified"** from the action dropdown and run it.

### Export applicants for one or more jobs

1. In the Jobs admin list, check the jobs you want to export applicants for.
2. Choose the **Export applicants for selected jobs to CSV** action.
3. The browser will download `applicants.csv` with `Job Title, Applicant Username, Applicant Email, Phone, Status, Applied At`.

---

## 9. Accounts (auth) — views, templates & flows

Routes (in `accounts/urls.py`):

```py
path('signup/employer/', views.employer_signup, name='employer_signup')
path('signup/seeker/', views.jobseeker_signup, name='jobseeker_signup')
path('login/', views.user_login, name='login')
path('logout/', views.user_logout, name='logout')
```

**Templates:**

* `templates/accounts/employer_signup.html`
* `templates/accounts/jobseeker_signup.html`
* `templates/accounts/login.html`
* `templates/accounts/logout.html`

**Behavior:**

* After signup the user is logged in automatically and redirected (`employer` → employer dashboard, `jobseeker` → job list).
* Login view redirects users by `role` (employer → dashboard, jobseeker → jobs list).

**Common template issue:** `TemplateDoesNotExist` — make sure `TEMPLATES.DIRS` includes `BASE_DIR / 'templates'` and templates live in `templates/accounts/`.

---

## 10. Employers — dashboard & job management flow

**URLs (jobs app):**

```py
path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard')
path('employer/job/create/', views.create_job, name='create_job')
path('employer/job/<uuid:pk>/edit/', views.edit_job, name='edit_job')
path('employer/job/<uuid:job_pk>/applications/', views.view_applications, name='view_applications')
path('employer/application/<int:app_pk>/status/', views.change_application_status, name='change_application_status')
```

**What employer can do:**

* Create & edit job posts using the `JobForm`.
* View list of jobs posted by the employer on the dashboard.
* View applications per job (see resume, cover letter, applicant info).
* Change application status (`APPLIED`, `SHORTLISTED`, `REJECTED`, `HIRED`).

**Access control:** employer-only pages are protected by `@login_required` and a simple `employer_required` decorator that checks `request.user.role == 'employer'`.

---

## 11. Job Seekers — search, view, apply flows

**URLs (jobs app):**

```py
path('', views.job_list, name='list')
path('job/<uuid:pk>/<slug:slug>/', views.job_detail, name='detail')
path('job/<uuid:pk>/apply/', views.apply_job, name='apply')
path('my/applications/', views.my_applications, name='my_applications')
```

**job_list** supports filtering by `q` (keyword), `location`, `category`, `company` parameters via GET. Results are paginated.

**job_detail** renders details and shows an Apply button if the logged-in user is a jobseeker.

**apply_job** prevents duplicate applications (`unique_together` enforced on `(job, applicant)`), accepts `resume` upload and `cover_letter`.

**my_applications** shows the candidate their applied jobs and statuses.

---

## 12. Forms, file uploads & validation

**Resume validation** (recommended):

```py
from django.core.validators import FileExtensionValidator
resume = models.FileField(upload_to='resumes/', validators=[FileExtensionValidator(['pdf','doc','docx'])])
```

**File size validator** (example):

```py
from django.core.exceptions import ValidationError

def validate_file_size(value):
    limit = 5 * 1024 * 1024  # 5 MB
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 5 MiB.')

resume = models.FileField(upload_to='resumes/', validators=[FileExtensionValidator(['pdf','doc','docx']), validate_file_size])
```

 **Important** : Never trust file names — verify extensions & MIME type on the server if security is critical.

---

## 13. Signals (auto-create EmployerProfile)

To auto-create an `EmployerProfile` when a User with role `employer` is created, add a signal handler:

```py
# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, EmployerProfile

@receiver(post_save, sender=User)
def create_employer_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'employer':
        EmployerProfile.objects.create(user=instance, company_name=instance.username)
```

Register signals in `accounts/apps.py` `ready()` method:

```py
# accounts/apps.py
from django.apps import AppConfig

class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        import accounts.signals
```

Then ensure `accounts.apps.AccountsConfig` is used in `INSTALLED_APPS`.

---

## 14. Templates & static files (how to organize; theme)

**Templates folder** (recommended):

```
templates/
├─ base.html
├─ accounts/
│  ├─ employer_signup.html
│  ├─ jobseeker_signup.html
│  ├─ login.html
│  └─ logout.html
├─ jobs/
│  ├─ job_list.html
│  ├─ job_detail.html
│  ├─ apply.html
│  └─ employer/*
```

**Base template** (`templates/base.html`) should provide the global layout and load static CSS/JS. Example minimal base that links a compiled `static/css/main.css`.

 **Static files** : move the embedded CSS in templates to `static/css/main.css` and reference it in `base.html`:

```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/main.css' %}">
```

 **Recommended workflow** : during development you can keep inline styles. For production, place CSS under `static/css/` and run `python manage.py collectstatic`.

---

## 15. Media handling & production storage (S3 suggestion)

Local dev: `MEDIA_ROOT` serves user uploads. In production, store media on S3 (or another object store). Use `django-storages` with `boto3`:

```ini
# pip install django-storages[boto3]
```

Configure `DEFAULT_FILE_STORAGE` and S3 credentials in env vars for production.

---

## 16. Security checklist & best practices

* **Never** commit `.env` or `SECRET_KEY` into git. Use environment variables.
* Set `DEBUG = False` in production.
* Configure `ALLOWED_HOSTS` appropriately.
* Use HTTPS (Let's Encrypt) and `SECURE_SSL_REDIRECT = True`.
* Set `SESSION_COOKIE_SECURE = True` and `CSRF_COOKIE_SECURE = True`.
* Use `django.middleware.security.SecurityMiddleware`.
* Validate uploaded files — type and size.
* Use password validators in `AUTH_PASSWORD_VALIDATORS`.
* Rate-limit critical endpoints if needed (login, apply) to prevent abuse.

---

## 17. Deployment notes (gunicorn, nginx, collectstatic, Docker)

 **Simple Gunicorn + Nginx example** :

```sh
# install gunicorn
pip install gunicorn

# run gunicorn (from project root)
gunicorn jobportal.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

**Nginx** should serve static & media and proxy pass to Gunicorn. On deploy, run:

```sh
python manage.py collectstatic --noinput
```

 **Docker** : Create `Dockerfile` and `docker-compose.yml` for quick reproducible deployments — consider Postgres as DB service and S3 for media.

**Using WhiteNoise** for serving static files directly from Django (good for simple deployments):

```py
# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    ...
]
```

---

## 18. Tests, migrations and fixtures

* Create tests under each app `tests.py` or tests/ folder and run with `pytest` or `python manage.py test`.
* Keep migrations in version control unless you intentionally want to regenerate them.
* Example fixtures command to dump sample data:

```bash
python manage.py dumpdata jobs.Category --indent 2 > fixtures/categories.json
python manage.py loaddata fixtures/categories.json
```

---

## 19. Troubleshooting common errors

### `TemplateDoesNotExist`

* Ensure `TEMPLATES.DIRS` contains `BASE_DIR / 'templates'`.
* Template path must match the render call, e.g. `render(request, 'accounts/employer_signup.html', ...)` requires `templates/accounts/employer_signup.html`.

### Migration errors

* If you change `AUTH_USER_MODEL` after creating migrations, you may have to reset migrations locally or carefully create compatible migrations.

### Static files not found in production

* Run `collectstatic` and check that `STATIC_ROOT` is writable.

### File upload 404 for media

* In dev with `DEBUG=True`, add `urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` to `urls.py`.

---

## 20. Useful commands summary

```bash
# python environment
python -m venv .venv
source .venv/bin/activate

# manage
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
python manage.py collectstatic --noinput

# shell
python manage.py shell
from accounts.models import User

# dump/load fixtures
python manage.py dumpdata jobs.Category > categories.json
python manage.py loaddata categories.json
```

---

## 21. Extending the project (next features)

* Add REST API with Django REST Framework for mobile apps.
* Add email notifications when applications arrive (Celery + Redis for background tasks).
* Add payment integration (Razorpay/Stripe) for featured jobs.
* Add full-text search (Postgres `tsvector`, or Elasticsearch/OpenSearch).
* Implement social login (Google/GitHub) for easier onboarding.
* Add analytics & admin dashboard charts (recharts / chart.js).

---

## 22. License & contribution

This project uses the **MIT License** (see `LICENSE` file). Contributions are welcome — open a PR with clear tests and documentation.

---

### Final notes

This README focuses on how to use and manage the Django admin and the provided HTML pages. If you want, I can:

* Generate `Dockerfile` and `docker-compose.yml`.
* Add a `base.html` template and extract the CSS into `static/css/main.css`.
* Create the sample fixture files and admin sample data.
* Add CI config (GitHub Actions) and linting (flake8/black).

Pick any follow-up and I will add it directly into the repo docs.
