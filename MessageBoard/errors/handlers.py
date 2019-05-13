from flask import Blueprint, render_template
import logging 

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
formatter = logging.Formatter('%(levelname)s:%(message)s:%(asctime)s')
file_handler = logging.FileHandler('errors_handlers.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def error_404(error):
	return render_template('custom_error_pages/404.html'),404

@errors.app_errorhandler(403)
def error_403(error):
	return render_template('custom_error_pages/403.html'),403

@errors.app_errorhandler(500)
def error_500(error):
	logger.warning(f'500 Error page raised at ')
	return render_template('custom_error_pages/500.html'),500