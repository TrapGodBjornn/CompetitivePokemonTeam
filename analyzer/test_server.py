from flask import Flask, make_response
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def test_home():
    response = make_response(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Page {datetime.now().strftime('%H:%M:%S')}</title>
        <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
        <meta http-equiv="Pragma" content="no-cache">
        <meta http-equiv="Expires" content="0">
    </head>
    <body>
        <h1>The Battle Lab Test at {datetime.now().strftime('%H:%M:%S')}</h1>
        <p>If you see this, the server is working correctly.</p>
    </body>
    </html>
    """)
    
    # Set cache control headers
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__ == '__main__':
    print("Starting test server on port 5000...")  # Changed port
    app.run(host='0.0.0.0', port=5000, debug=True) 