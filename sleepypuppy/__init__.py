from logging import Formatter
from logging.handlers import RotatingFileHandler
from flask import Flask, redirect, request, abort, send_from_directory
from flask.ext import login
from flask.ext.bcrypt import Bcrypt
from flask.ext.restful import Api
from flask.ext.admin import Admin
from flask.ext.mail import Mail
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
from flask_sslify import SSLify
import flask_wtf

# Config and App setups
app = Flask(__name__)
app.config.from_object('config-default')
app.config.update(dict(
  PREFERRED_URL_SCHEME = 'https'
))
app.debug = app.config.get('DEBUG')
# Log handler functionality
handler = RotatingFileHandler(app.config.get('LOG_FILE'), maxBytes=10000000, backupCount=100)
handler.setFormatter(
    Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    )
)
handler.setLevel(app.config.get('LOG_LEVEL'))
app.logger.addHandler(handler)

# HSTS
#sslify = SSLify(app)

#SSL
from functools import wraps
from flask import request, redirect, current_app

def ssl_required(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if app.config.get("SSL"):
            if request.is_secure:
                return fn(*args, **kwargs)
            else:
                return redirect(request.url.replace("http://", "https://"))
        
        return fn(*args, **kwargs)
            
    return decorated_view

# CSRF Protection
csrf_protect = flask_wtf.CsrfProtect(app)

# Initalize DB object
db = SQLAlchemy(app)

# Initalize Bcrypt object for password hashing
bcrypt = Bcrypt(app)

# Initalize flask mail object for email notifications
flask_mail = Mail(app)

# Decorator for Token Auth on API Requests
from sleepypuppy.admin.admin.models import Administrator
from sleepypuppy.admin.assessment.models import Assessment


# The dectorat function for API token auth
def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.headers.get('Token'):
            for keys in Administrator.query.all():
                print keys.api_key
                if request.headers.get('Token') == keys.api_key:
                    return view_function(*args, **kwargs)
            abort(401)
        else:
            abort(401)
    return decorated_function

# Initalize the Flask API
flask_api = Api(app, decorators=[csrf_protect.exempt, require_appkey])


# Initalize Flask Login functionality
def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)
    login_manager.session_protection = "strong"

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(Administrator).get(user_id)

# Intalize the login manager for sleepy puppy
init_login()

# Create the Flask Admin object
from admin.admin.views import MyAdministratorIndexView, AdministratorView
flask_admin = Admin(app, 'Sleepy Puppy', index_view=MyAdministratorIndexView(), base_template='admin/base.html', template_mode='bootstrap3')

# Import the collector which is used to collect capture information
from collector import views

# Import the screenshot upload handler
from upload import upload

# # Initalize all Flask API views
from api.views import CaptureView, CaptureViewList, PayloadView, PayloadViewList, AssessmentView, AssessmentViewList
flask_api.add_resource(AssessmentViewList, '/api/assessments')
flask_api.add_resource(AssessmentView, '/api/assessments/<int:id>')
flask_api.add_resource(CaptureViewList, '/api/captures')
flask_api.add_resource(CaptureView, '/api/captures/<int:id>')
flask_api.add_resource(PayloadViewList, '/api/payloads')
flask_api.add_resource(PayloadView, '/api/payloads/<int:id>')

# # Initalize all Flask Admin dashboard views
from admin.capture.views import CaptureView
from admin.payload.views import PayloadView
from admin.user.views import UserView
from admin.assessment.views import AssessmentView

from sqlalchemy.orm import configure_mappers
configure_mappers()

# # Add all Flask Admin routes
flask_admin.add_view(PayloadView(db.session))
flask_admin.add_view(CaptureView(db.session))
flask_admin.add_view(UserView(db.session))
flask_admin.add_view(AssessmentView(db.session))
flask_admin.add_view(AdministratorView(Administrator, db.session))
from admin import views

# Default route redirect to admin page

@app.route('/')
def index():
    return redirect('/admin', 302)

@app.route('/assets/<path:filename>')
def send_js(filename):
    print send_from_directory(app.config['ASSETS_FOLDER'], filename)
    return send_from_directory(app.config['ASSETS_FOLDER'], filename)

