Google OAuth setup (django-allauth)

This repository includes a minimal django-allauth configuration. To enable Google Sign-In end-to-end do the following:

1. Install the package (in your virtualenv):

   pip install django-allauth

2. Add migrations & migrate:

   py -3 manage.py migrate

3. Create a Google OAuth client:
   - Go to https://console.developers.google.com/
   - Create or select a project
   - Navigate to "OAuth consent screen" and configure the app (internal/testing)
   - Under "Credentials" create an "OAuth 2.0 Client ID" of type Web application
   - Add an Authorized redirect URI, e.g.:
     http://127.0.0.1:8000/accounts/google/login/callback/
   - Save Client ID and Client Secret

4. Configure django-allauth SocialApp (two options):

   Option A: via Django admin
   - Run the dev server and log in to admin
   - Go to Social applications -> Add Social Application
     * Provider: Google
     * Name: Google
     * Client id: <your-client-id> 783123698567-0qrq34vooq3dd8fs5keo9i9fmovfqfm1.apps.googleusercontent.com
     * Secret key: <your-client-secret>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
     * Sites: select the site (example.com or example localhost site)

   Option B: via code or fixtures
   - You can create a `SocialApp` model instance in a migration or a management command.

5. Ensure your site's domain matches the redirect URI and the SocialApp 'Sites' entry.

6. (Optional) Set environment variables for production and secure storage of secrets.

Notes and troubleshooting
- If you see a redirect URI mismatch error, double-check the URI configured in Google Console and the callback used by django-allauth.
- In production, use HTTPS for OAuth redirect URIs.
- For custom templates, override `account/login.html` to add a "Login with Google" button linking to `/accounts/google/login/`.

If you'd like, I can:
- Add a short `SocialApp` creation migration for development that reads env vars and auto-creates the SocialApp.
- Add a custom login template that shows a "Sign in with Google" button wired to allauth.
