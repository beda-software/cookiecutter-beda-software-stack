import pytz
import os

app_superadmin_email = os.environ.get("APP_SUPERADMIN_EMAIL", "admin@health-samurai.io")
app_superadmin_password = os.environ.get(
    "APP_SUPERADMIN_PASSWORD", os.environ.get("AIDBOX_ADMIN_PASSWORD")
)

secret_key = os.environ.get("SECRET_KEY", "").encode()
local_tz = pytz.timezone(os.environ.get("LOCAL_TZ", "US/Central"))

from_email = os.environ.get("FROM_EMAIL", "donotreply@example.com")

frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:3000")
backend_public_url = os.environ.get("BACKEND_PUBLIC_URL", "http://localhost:8080")

{% if cookiecutter.add_gcs|lower == 'y' %}
gc_bucket = os.environ.get("BUCKET", "")
gc_account_file = os.environ.get("BUCKET_ACCOUNT_PATH", "") or os.environ.get(
    "GOOGLE_APPLICATION_CREDENTIALS", ""
)
{% endif %}

{% if cookiecutter.add_aws|lower == 'y' %}
aws_bucket = os.environ.get("AWS_BUCKET")
aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
{% endif %}

{% if cookiecutter.add_google_oauth|lower == 'y' %}
google_oauth_app_id = os.environ.get("GOOGLE_OAUTH_APP_ID")
google_oauth_app_secret = os.environ.get("GOOGLE_OAUTH_APP_SECRET")
{% endif %}

{% if cookiecutter.add_postmark|lower == 'y' %}
postmark_api_token = os.environ.get("POSTMARK_API_TOKEN")
postmark_email_from = os.environ.get("POSTMARK_EMAIL_FROM")
{% endif %}

{% if cookiecutter.add_twilio|lower == 'y' %}
twilio_sid = os.environ.get("TWILIO_SID", "")
twilio_token = os.environ.get("TWILIO_TOKEN", "")
twilio_phone_number = os.environ.get("TWILIO_PHONE_NUMBER", "")
twilio_sender_name = os.environ.get("TWILIO_SENDER_NAME", "")
use_fake_sms_code = not twilio_token
{% endif %}

{% if cookiecutter.add_push_notifications|lower == 'y' %}
fcm_sender_id = os.environ.get("FCM_SENDER_ID", "")
fcm_api_key = os.environ.get("FCM_API_KEY", "")
apns_pem_file = os.environ.get("APNS_PEM_FILE", "")
use_sandbox = os.environ.get("APNS_SANDBOX", "True") == "True"
{% endif %}

root_dir = os.path.dirname(os.path.abspath(__name__))

dev_init = os.environ.get("DEV_INIT", "False") == "True"
environment_name = os.environ.get("SENTRY_ENVIRONMENT", "")
