from flask import (
    Blueprint
)
from app.log.log import Log

bp = Blueprint('log', __name__, url_prefix='/log')

print('show_log has been loaded')

@bp.route('/show')
def show_log():
    return Log.read().replace('\n', '<br \>')