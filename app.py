from flask import Flask, render_template, request, send_file
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Flask receives a single file per POST request from JS
        file = request.files.get('file')
        if file:
            # Save the uploaded Excel file
            input_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(input_path)

            # Read Excel and convert to CSV
            df = pd.read_excel(input_path)
            output_path = input_path.rsplit(".", 1)[0] + ".csv"
            df.to_csv(output_path, index=False)

            # Send CSV file to browser for download
            return send_file(output_path, as_attachment=True)

    # GET request: render the main page
    return render_template("index.html")

if __name__ == "__main__":
    # Run on all network interfaces so it can be accessed on mobile/other devices
    app.run(debug=True, host="0.0.0.0", port=8000)
