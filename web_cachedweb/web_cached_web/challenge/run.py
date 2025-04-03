from application.database import get_db
from application.main import app

with app.app_context():
    with app.open_resource('schema.sql', mode='r') as f:
        get_db().cursor().executescript(f.read())
        
app.run(host='0.0.0.0', port=1337, debug=True, use_evalex=False)