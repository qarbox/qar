
from flask import Blueprint, render_template

bp = Blueprint('wizard', __name__)

@bp.route('/')
def dashboard():
    steps = [
        {"key": "welcome", "label": "Welcome"},
        {"key": "language", "label": "Language"},
        {"key": "disk", "label": "Disk"},
        {"key": "internet", "label": "Internet"},
        {"key": "vpn", "label": "VPN"},
        {"key": "quality", "label": "Quality"},
        {"key": "limits", "label": "Limits"},
        {"key": "review", "label": "Review"}
    ]

    return render_template('wizard.html', title='Wizard', steps=steps)
