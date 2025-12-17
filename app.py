from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import pandas as pd
import os
import re

app = Flask(__name__)
app.secret_key = "supersecretkey"  # required for flash messages

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def validate_excel(df):
    errors = []
    
    # Check Name column (only letters)
    if 'Name' in df.columns:
        for i, name in enumerate(df['Name'], start=2):
            if not isinstance(name, str) or not re.match(r"^[A-Za-z\s]+$", str(name)):
                errors.append(f"Row {i}: Invalid Name '{name}'")

    # Check Mobile column (only numbers, 10 digits)
    if 'Mobile' in df.columns:
        for i, mobile in enumerate(df['Mobile'], start=2):
            if not str(mobile).isdigit() or len(str(int(mobile))) != 10:
                errors.append(f"Row {i}: Invalid Mobile '{mobile}'")

    # Check Gender column (must be 'Male' or 'Female')
    if 'Gender' in df.columns:
        for i, gender in enumerate(df['Gender'], start=2):
            if str(gender).strip().capitalize() not in ['Male', 'Female']:
                errors.append(f"Row {i}: Invalid Gender '{gender}'")
    
    return errors

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get('file')
        if file:
            input_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(input_path)

            try:
                df = pd.read_excel(input_path)
            except Exception as e:
                flash(f"Error reading Excel file: {str(e)}")
                return redirect(url_for('index'))

            errors = validate_excel(df)
            if errors:
                # Show errors to user
                return render_template("index.html", errors=errors)

            output_path = input_path.rsplit(".", 1)[0] + ".csv"
            df.to_csv(output_path, index=False)
            return send_file(output_path, as_attachment=True)

    return render_template("index.html", errors=None)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
