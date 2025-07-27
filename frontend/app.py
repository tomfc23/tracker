from flask import Flask, render_template, request, send_from_directory
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
OUTPUT_FOLDER = 'static/outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['video']
    filename = file.filename
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_path = os.path.join(OUTPUT_FOLDER, f"tracked_{filename}")
    file.save(input_path)

    # Run the tracker script
    subprocess.run([
        "python3.13", "track.py",
        "--source", input_path,
        "--yolo-model", "yolov5s.pt",
        "--save-vid",
        "--project", OUTPUT_FOLDER,
        "--name", f"tracked_{filename}",
        "--exist-ok"
    ])

    return f'''
        <h3>Tracking Complete</h3>
        <video width="640" controls>
          <source src="/static/outputs/tracked_{filename}/tracked_{filename}.mp4" type="video/mp4">
        </video><br>
        <a href="/">Back</a>
    '''

@app.route('/static/outputs/<path:filename>')
def download(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
