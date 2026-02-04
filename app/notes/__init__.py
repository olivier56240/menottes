from flask import Blueprint

bp = Blueprint("notes", __name__, url_prefix="/notes")

from . import routes  # noqa