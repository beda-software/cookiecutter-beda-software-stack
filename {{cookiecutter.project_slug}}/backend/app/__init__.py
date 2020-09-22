{% if cookiecutter.add_gcs|lower == 'y' %}import app.gcs{% endif %}
{% if cookiecutter.add_aws|lower == 'y' %}import app.aws{% endif %}
import app.notification
