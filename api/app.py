from flask import Flask, jsonify, render_template
from routes import register_routes
from db import close_db_connection
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from log_config import setup_logging

setup_logging()

app = Flask(__name__, template_folder="templates")  # Ensure templates folder is set

app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per minute"]
)

register_routes(app, cache, limiter)

@app.teardown_appcontext
def close_connection(exception):
    close_db_connection()

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Not Found", "message": "The requested resource was not found."}), 404

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        "error": "Too Many Requests",
        "message": "You have exceeded your request limit. Please try again later."
    }), 429

if __name__ == '__main__':
    app.run(debug=True)
