from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///top_scorer.db"
app.secret_key = "my_secret_key"

db = SQLAlchemy(app)


class Scorer(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), nullable=False, unique=False)
    goals = db.Column(db.Integer, nullable=False, unique=False)
    assists = db.Column(db.Integer, nullable=False, unique=False)


db.create_all()


@app.route('/')
def home():
    all_scorers = db.session.query(Scorer).all()
    return render_template("index.html", scorers=all_scorers)


@app.route("/add", methods=["POST", "GET"])
def add_player():
    if request.method == "POST":
        new_player = Scorer(
            name=request.form["name"],
            goals=request.form["goals"],
            assists=request.form["assists"]
        )

        db.session.add(new_player)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)
