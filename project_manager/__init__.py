from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_mysqldb import MySQL


from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = '683acd1c8b1ee1fbd830be0e99adce24'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:admin@127.0.0.1:2202/project_management'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'DB://UNAME:PASSWORD@HOST/DB_NAME'


# MYSQL LOCAL
# app.config['MYSQL_HOST'] = '127.0.0.1'
# app.config['MYSQL_PORT'] = 2202
# app.config['MYSQL_USER'] = 'admin'
# app.config['MYSQL_PASSWORD'] = 'admin'
# app.config['MYSQL_DB'] = 'project_management'



db = SQLAlchemy(app)

migrate = Migrate(app,db)
# db = MySQL(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from project_manager import routes