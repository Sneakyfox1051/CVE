from flask import Blueprint, jsonify, request, abort, render_template
from functools import wraps
from db import query_db
import queries  # Import the queries
from math import ceil

def register_routes(app, cache, limiter):
    @app.route('/')
    def home():
        return render_template('index.html')  # Renders a front-end page

    @app.route('/cves/list', methods=['GET'])
    @limiter.limit("20 per minute")  # Rate limit: 20 requests per minute per IP
    @cache.cached(timeout=1)  # Cache this route for 60 seconds
    def get_vulnerabilities():
        # Retrieve parameters from the request
        page = request.args.get('page', default=1, type=int)  # Retrieve the page parameter, default to 1
        rows = request.args.get('rows', default=10, type=int)  # Retrieve the rows parameter, default to 10

        # Validate the rows parameter
        if rows not in [10, 50, 100]:
            abort(400, description="Invalid number of rows. Please select from 10, 50, or 100.")

        # Execute the query to get the total count of vulnerabilities
        total_count_result = query_db(queries.get_total_vulnerabilities_count())

        # Check if we received a result and extract the count
        if total_count_result:
            total_count = total_count_result[0]['total']  # Assuming query_db returns a list of dictionaries
        else:
            total_count = 0  # Default to 0 if no result is found

        # Calculate total pages
        total_pages = ceil(total_count / rows)

        # Get vulnerabilities for the current page
        results = query_db(queries.get_all_vulnerabilities(page, rows))

        # Return the results in JSON format
        return jsonify({
            'data': results,
            'current_page': page,
            'total_pages': total_pages,
            'total_count': total_count
        })

    @app.route('/cves/id/<int:id>', methods=['GET'])
    @limiter.limit("20 per minute")  # Rate limit: 20 requests per minute per IP
    def get_metrics_by_id(id):
        # Query the metrics associated with the given ID
        metrics = query_db(queries.get_metrics_by_id(id), (id,))  # Pass the ID as an argument

        # Check if any metrics were found
        if not metrics:
            abort(404, description="Metrics not found for the specified ID.")

        # Return the metrics in JSON format
        return jsonify(metrics)
