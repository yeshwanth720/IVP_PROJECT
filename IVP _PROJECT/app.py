from flask import Flask,render_template, request
import rough
app = Flask(__name__)

def create_app():
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/process_url", methods=["POST"])
    def process_url():
        url = request.form.get("url")
        return render_template("result.html", url=url)

    return app

if __name__ == "__main__":
    create_app().run(debug=True)