from app import app
from flask import url_for 
from config import REVPROX
#if REVPROX == True:
#    app.run(host='127.0.0.1', port=8080)
#else:
app.run(host='0.0.0.0', port=80)
#app.run(debug=True, host='0.0.0.0')
