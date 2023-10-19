from app import app, database
from views import *
from models import *


if __name__ == '__main__':
    create_tables()
    app.run(host='0.0.0.0')
