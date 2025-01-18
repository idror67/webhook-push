from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Path to store the webhook logs
OUTPUT_DIR = '/opt/simpleFlask'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'webhook_data.json')

# Ensure the directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming webhook data."""
    print("Received webhook data", flush=True)

    try:
        # Get the JSON payload from the webhook
        webhook_data = request.get_json()
        if not webhook_data:
            print("No JSON payload received", flush=True)
            return 'Webhook received but no data', 400  # Bad Request

        # Extract required information
        repository_name = webhook_data.get('repository', {}).get('name', 'Unknown repository')
        head_commit = webhook_data.get('head_commit', {})
        commit_id = head_commit.get('id', 'Unknown commit ID')
        changed_files = head_commit.get('modified', [])

        # Log the extracted data
        print(f"Repository Name: {repository_name}", flush=True)
        print(f"Commit ID: {commit_id}", flush=True)
        print(f"Changed Files: {changed_files}", flush=True)

        # Store the filtered data in a structured format
        filtered_data = {
            'repository_name': repository_name,
            'commit_id': commit_id,
            'changed_files': changed_files
        }

        # Append data to the logs file
        if os.path.exists(OUTPUT_FILE):
            with open(OUTPUT_FILE, 'r') as f:
                logs = json.load(f)
        else:
            logs = []

        logs.append(filtered_data)

        with open(OUTPUT_FILE, 'w') as f:
            json.dump(logs, f, indent=4)
        
        print(f"Data saved to {OUTPUT_FILE}", flush=True)
        return 'Webhook received and data logged', 200

    except Exception as e:
        # Log the exception and return a 500 response
        print(f"Error: {e}", flush=True)
        return 'Internal Server Error', 500

@app.route('/logs', methods=['GET'])
def display_logs():
    """Display logs as a styled HTML page."""
    # Load the logs
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r') as f:
            logs = json.load(f)
    else:
        logs = []

    # Generate HTML dynamically
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Webhook Logs</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                margin: 0;
                padding: 0;
                color: #333;
            }
            .container {
                max-width: 1200px;
                margin: 50px auto;
                padding: 20px;
                background: #fff;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            h1 {
                text-align: center;
                color: #444;
                margin-bottom: 20px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                font-size: 16px;
            }
            table th, table td {
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }
            table thead tr {
                background-color: #007BFF;
                color: #fff;
            }
            table tbody tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            table tbody tr:hover {
                background-color: #f1f1f1;
            }
            ul {
                padding-left: 20px;
                margin: 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Webhook Logs</h1>
    """
    if logs:
        html += """
            <table>
                <thead>
                    <tr>
                        <th>Repository Name</th>
                        <th>Commit ID</th>
                        <th>Changed Files</th>
                    </tr>
                </thead>
                <tbody>
        """
        for log in logs:
            html += f"""
                    <tr>
                        <td>{log['repository_name']}</td>
                        <td>{log['commit_id']}</td>
                        <td>
                            <ul>
            """
            for file in log.get('changed_files', []):
                html += f"<li>{file}</li>"
            html += """
                            </ul>
                        </td>
                    </tr>
            """
        html += """
                </tbody>
            </table>
        """
    else:
        html += "<p>No logs available.</p>"
    html += """
        </div>
    </body>
    </html>
    """
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)