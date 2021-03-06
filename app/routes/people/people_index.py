from flask import Blueprint, render_template
from flask_login import login_required
from utils import require_role
from . import page
from . import accepted_roles





@page.route("/")
@login_required
@require_role(accepted_roles)
def index():
    """Only allow admin users"""
    # Otherwise, proceed
    return render_template('people/people-index.html',title='People')

















#
