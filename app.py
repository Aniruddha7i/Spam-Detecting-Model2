from flask import Flask, render_template

app: Flask = Flask(__name__, template_folder='template', static_folder='static')


@app.route("/")
def lode_home_page():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
