# CleanTrack — Presentation Notes

> Concise, printable notes for your presentation on the CleanTrack Django project.

---

## 1. Project Summary ✅
- CleanTrack is a Django app that allows citizens to report public littering using video evidence.
- Flow: Register (OTP verification) → Login → Submit Report (video, location, description) → Admin review → Approve → Reward points (user).
- Stack: Django (custom User model), SQLite (dev), file uploads (MEDIA), SMTP email for OTPs, templates + CSS for UI.

---

## 2. Quick User Workflow 🔁
1. User registers at `/register/` → account created with `is_active = False`, OTP generated and emailed (10 min expiry).
2. User verifies OTP at `/verify-otp/<email>/` → account activated.
3. User logs in and opens `/dashboard/` → submits `ReportForm` (location, description, video).
4. Admin reviews reports in `/admin/` and uses **Approve** action to set `status='Approved'` and add `reward_points`.
5. User views submissions at `/my-reports/`.

---

## 3. Important files & purpose (one-liners) 🔧
- `manage.py` — run server, migrations, tests.
- `waste_management/settings.py` — configuration (DB, static/media, email, AUTH_USER_MODEL). Move secrets to env vars.
- `waste_management/urls.py` — root URL router.
- `core/models.py` — `User` (custom fields: otp, reward_points, mobile, age, gender), `Report` model (video, status, created_at).
- `core/forms.py` — `CustomUserCreationForm` (validations) and `ReportForm`.
- `core/views.py` — request handlers: `register`, `verify_otp`, `resend_otp`, `dashboard`, `my_reports`.
- `core/urls.py` — app routes: `register`, `login`, `dashboard`, `verify-otp`, `resend-otp`.
- `core/admin.py` — admin site + actions (`approve_reports`, `reject_reports`).
- `core/templates/` — `base.html`, `dashboard.html`, `my_reports.html`, `registration/*` templates.
- `static/css/style.css` — site theme and tricolor visuals.
- `media/` — uploaded videos (upload path: `reports/`).

---

## 4. Key functions & their behavior 🧾
- `register(request)`
  - Creates inactive user, sets `otp` and `otp_expires = now + 10min`, sends email, redirects to verify.
- `verify_otp(request, email)`
  - Checks `user.otp == entered_otp` and `user.otp_expires > now`; sets `is_active=True` on success.
- `resend_otp(request, email)`
  - Generates new OTP and updates expiry; re-sends OTP email.
- `dashboard(request)`
  - Auth-required; handles `ReportForm` POST and lists user's reports (ordered by newest).
- `ReportAdmin.approve_reports(request, queryset)`
  - Marks reports as `Approved`, increments `user.reward_points` by 10 per approved report.

---

## 5. Security & Production best practices 🔒
- **Environment variables:** never put secrets (SECRET_KEY, EMAIL_HOST_PASSWORD) in `settings.py`. Use `os.environ` or `django-environ`. Benefits: avoids git leaks, allows rotation, and reduces blast radius.
- **OTP security:** store OTP carefully (consider hashing), mark as used, apply rate limiting and lockouts.
- **Email & background jobs:** send email asynchronously (Celery/RQ) in production.
- **File uploads:** validate mime/type and size, scan files, use cloud storage (S3) + signed URLs in prod.
- **Settings:** set `DEBUG=False` and configure `ALLOWED_HOSTS` in production.

---

## 6. Templates & CSS — important points ✨
- Template inheritance: `base.html` contains header/footer and defines blocks such as `{% block content %}`. Child templates: `{% extends 'core/base.html' %}` + `{% block content %}`.
- Useful template tags: `{% csrf_token %}`, `{% url 'name' %}`, filters like `|date:"d M Y"`.
- CSS notes: `style.css` uses CSS variables (`:root`) for theme colors: `--saffron`, `--green`, `--indigo`, `--accent`.
- Tricolor effect: created via `--tricolor: linear-gradient(90deg,var(--saffron) 0%, #ffffff 50%, var(--green) 100%);` and can be applied to `body::before` or `.btn-primary`.

---

## 7. Demo script (2–3 min) 🎯
1. Open site home (show `base.html` header + hero).  
2. Show `Register` → `register.html` → explain OTP generation (show in DB if dev).  
3. Verify OTP → login → go to `dashboard` → submit a small video with location.  
4. Admin panel → select report → Approve → show `reward_points` increment.  

---

## 8. Practice Q&A (short answers) 💬
- Q: Why custom user model?  
  A: To add fields (otp, reward_points, mobile, age) and enforce unique email early.
- Q: How to prevent OTP brute force?  
  A: Rate limit attempts, expire OTP quickly, mark OTP used, and lock after repeated fails.
- Q: How to scale file storage?  
  A: Use S3, signed URLs, CDN, and process videos asynchronously.
- Q: Why use env vars?  
  A: Prevents secrets in git, supports rotation, and reduces exposure across environments.

---

## 9. Commands & quick dev tips ⚙️
- Activate venv (Windows PowerShell): `& .venv\Scripts\Activate.ps1`  
- Run dev server: `python manage.py runserver`  
- Make migrations: `python manage.py makemigrations` → `python manage.py migrate`  
- Create superuser: `python manage.py createsuperuser`

---

## 10. One-page checklist to show in talk ✅
- Explain app purpose & flow.  
- Show `register()` OTP logic, `verify_otp()`, and `dashboard()` flow.  
- Show admin approve action and `reward_points` change.  
- Mention security improvements (env vars, background email, S3).  
- Suggest tests to add (OTP, forms, views, admin actions).

---

## 11. Next steps I can do for you (choose one) 🔧
- Create a 5‑slide presentation outline (titles + bullets).  
- Convert this note to PDF and add a 1‑page cheat sheet.  
- Add example unit tests for OTP flow and report submission.

---

**File location:** `docs/presentation_notes.md` (open it in VS Code or download/export as PDF).

If you want a PDF now, reply "Export PDF" and I'll create `docs/presentation_notes.pdf` for you. 

Good luck with your presentation — I can also make a short cheat-sheet you can print. ✨
