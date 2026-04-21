# Lab Inventory Manager - Setup Guide for Friends (VS Code)

Use this guide after you receive the project folder.

## 1. What you should receive

Your friend should share the full project folder with this structure:

- `manage.py`
- `requirements.txt`
- `labinventory/`
- `inventory/`
- `templates/`

Do not copy only single files. Copy the full folder.

## 2. Prerequisites (install once)

- Python 3.10+ installed
If you or I added a new model field (for example `status` on `LabItem`), run the app-specific makemigrations to ensure those fields are created:

```powershell
python manage.py makemigrations inventory
python manage.py migrate
```
- VS Code installed
- Python extension in VS Code

Check Python version in terminal:

```powershell
python --version
```

## 3. Open project in VS Code

1. Open VS Code
2. File -> Open Folder
3. Select the project folder (the one containing `manage.py`)
4. Open terminal in VS Code

## 4. Create virtual environment (recommended)

```powershell
python -m venv venv
```

Activate it:
```

If activation is blocked, run this once in PowerShell (as Administrator):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again.

6. Confirm the `status` field is available in the Add/Edit form and can be set to "In Stock", "Out of Stock" or "Damaged"
7. Use the **Export CSV** button on the dashboard to download a `lab_items.csv` file and verify it contains your items
## 5. Install dependencies

```powershell
pip install -r requirements.txt
```

## 6. Create database tables

Run these commands in this exact order:

```powershell
python manage.py makemigrations
python manage.py migrate
```

## 7. Create admin user

Normal way:

```powershell
python manage.py createsuperuser
```

Important: while typing password, nothing appears in terminal. This is normal.
Type password and press Enter.

If terminal still does not accept password, use this fallback:

```powershell
python create_superuser.py
### Note: Logout uses POST
```
The UI uses a small POST form for logout (with CSRF). Click the Logout button — it posts to the logout view and then redirects to login. If you see a 405 error, restart the server and ensure CSRF and sessions are enabled.

## 8. Start the project

```powershell
python manage.py runserver
```

Open the URL shown in terminal. Usually:

- `http://127.0.0.1:8000/`
- Login page: `http://127.0.0.1:8000/accounts/login/`
- Dashboard: `http://127.0.0.1:8000/dashboard/`

Important: `127.0.0.1` and `localhost` only work on the same laptop where Django is running. If you want other people to open the website from their own devices, you must deploy the project to a public hosting service and use the deployed URL instead.

## 9. Test checklist

After login:

1. Add a new item
2. Edit the item
3. Delete an item
4. Add one item with quantity below 5
5. Confirm low stock appears in red on dashboard

## 10. Common errors and fixes

### Error: `This site can't be reached`

Cause: server is not running.

Fix:

```powershell
python manage.py runserver
```

### Error: `no such table: inventory_labitem`

Cause: migrations not applied.

Fix:

```powershell
python manage.py makemigrations inventory
python manage.py migrate
```

### Error: password not visible while typing

Cause: normal terminal security behavior.

Fix: keep typing password and press Enter.

## 11. HTTP vs HTTPS

For Django local development, default URL is HTTP.

- HTTP example: `http://127.0.0.1:8000/`
- HTTPS is usually not enabled in default `runserver`

Also, `runserver` is meant for local testing only. It does not create a public internet link by itself.

So for this project and practical submission, use the HTTP local URL shown in terminal.

## 12. How to submit/share this project

Share the full project folder (zip preferred), including:

- code files
- template files
- `requirements.txt`
- this setup guide

Do not share `venv/` folder.

## 13. How to make it public

If you want other people to open the inventory site from their own devices, deploy it to a hosting service instead of using `runserver`.

Simple path:

1. Put the project on GitHub
2. Create a web app on PythonAnywhere, Render, or a similar host
3. Set environment variables like `SECRET_KEY`, `DEBUG=False`, and `ALLOWED_HOSTS`
4. Run migrations on the host
5. Collect static files
6. Open the public URL the host gives you

If you keep using `http://127.0.0.1:8000/`, the site will still only open on your own laptop.

---

If someone still has an issue, share:

1. full terminal error text
2. command they ran
3. screenshot of browser error page
