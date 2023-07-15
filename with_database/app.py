# from flask import Flask, render_template
# import connexion

# app = connexion.App(__name__, specification_dir="./")
# app.add_api("swagger.yml")
# @app.route("/")
# def home():
#     return render_template("home.html")

# if __name__ == "__main__":
#     app.run(debug=True)
    
#ADDING DATABASE
   
from flask import Flask, render_template
import config
from models import Person

app =config.connex__app
app.add_api(config.basedir / "swagger.yml")
@app.route("/")
def home():
    people = Person.query.all()
    return render_template("home.html", people=people)

if __name__ == "__main__":
    app.run(debug=True)