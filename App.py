from flask import Flask, request, jsonify
from Ask2 import search

app = Flask(__name__)


@app.route('/search')
def index():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'invalid username'})
    result = search(username)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1233)
