# ...server.py 
# you need will need to import all your controllers into the server file.
# you will need to import your app from the **"flask_app"** file 

from flask_app.controllers import login_controller
from flask_app import app

         
if __name__ == "__main__":
    app.run(debug=True)
