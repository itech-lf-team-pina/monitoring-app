from flask import (
    Blueprint
)
from .log import Log

bp = Blueprint('log', __name__, url_prefix='/log')

@bp.route('/show')
def show_log():
    return Log.read().replace('\n', '<br \>')