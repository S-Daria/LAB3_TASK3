from flask import Flask, render_template, request
from location_detector import make_csv_location
from friends_map import generate_map_with_csv

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def find_friend():
    if request.method == 'POST':
        username = request.form.get('username')
        token = request.form.get('key')
        make_csv_location(username, token)
        generate_map_with_csv()
        return render_template('friends_map.html')
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)