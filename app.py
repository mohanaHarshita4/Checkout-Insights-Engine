"""
E-Commerce Analytics Platform - Application Layer

This is a small Flask app that connects to the MySQL database and lets
you call the stored procedures through a web browser instead of typing
SQL commands manually. This satisfies the "connect an application to
MySQL" course outcome.
"""

import os
from flask import Flask, render_template_string
import mysql.connector

app = Flask(__name__)


DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "127.0.0.1"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD"),
    "database": os.environ.get("DB_NAME", "ecommerce_analytics")
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)



PAGE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: #333; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ccc; padding: 8px 12px; text-align: left; }
        th { background-color: #f4f4f4; }
        nav { margin-bottom: 20px; }
        nav a { margin-right: 15px; }
    </style>
</head>
<body>
    <nav>
        <a href="/">Home</a>
        <a href="/low-stock">Low Stock</a>
        <a href="/revenue/2026/8">Revenue (Aug 2026)</a>
        <a href="/customer/1">Customer 1 Lifetime Value</a>
        <a href="/ab-test-results">A/B Test Results</a>
    </nav>
    <h1>{{ title }}</h1>
    {% if rows %}
    <table>
        <tr>
            {% for col in columns %}<th>{{ col }}</th>{% endfor %}
        </tr>
        {% for row in rows %}
        <tr>
            {% for value in row %}<td>{{ value }}</td>{% endfor %}
        </tr>
        {% endfor %}
    </table>
    {% else %}
    <p>No results found.</p>
    {% endif %}
</body>
</html>
"""

@app.route("/")
def home():
    return """
    <h1>E-Commerce Analytics Platform</h1>
    <p>This is the application layer connecting to the MySQL backend.</p>
    <ul>
        <li><a href="/low-stock">Low Stock Alert</a></li>
        <li><a href="/revenue/2026/8">Monthly Revenue by Category (Aug 2026)</a></li>
        <li><a href="/customer/1">Customer Lifetime Value (Customer 1)</a></li>
        <li><a href="/ab-test-results">A/B Test Results</a></li>
    </ul>
    """

@app.route("/customer/<int:customer_id>")
def customer_lifetime_value(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.callproc("sp_customer_lifetime_value", [customer_id])

    columns = []
    rows = []
    for result in cursor.stored_results():
        columns = [desc[0] for desc in result.description]
        rows = result.fetchall()

    cursor.close()
    conn.close()

    return render_template_string(
        PAGE_TEMPLATE,
        title=f"Lifetime Value - Customer {customer_id}",
        columns=columns,
        rows=rows,
    )


@app.route("/low-stock")
def low_stock():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.callproc("sp_low_stock_alert")

    columns = []
    rows = []
    for result in cursor.stored_results():
        columns = [desc[0] for desc in result.description]
        rows = result.fetchall()

    cursor.close()
    conn.close()

    return render_template_string(
        PAGE_TEMPLATE, title="Low Stock Alert", columns=columns, rows=rows
    )


@app.route("/revenue/<int:year>/<int:month>")
def revenue(year, month):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.callproc("sp_monthly_revenue_by_category", [year, month])

    columns = []
    rows = []
    for result in cursor.stored_results():
        columns = [desc[0] for desc in result.description]
        rows = result.fetchall()

    cursor.close()
    conn.close()

    return render_template_string(
        PAGE_TEMPLATE,
        title=f"Revenue by Category - {month}/{year}",
        columns=columns,
        rows=rows,
    )


@app.route("/ab-test-results")
def ab_test_results():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ABTestResults")

    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template_string(
        PAGE_TEMPLATE, title="A/B Test Results", columns=columns, rows=rows
    )


if __name__ == "__main__":
    app.run(debug=True)
