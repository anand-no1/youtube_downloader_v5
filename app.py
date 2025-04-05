
from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        return "No URL provided", 400

    # Generate unique filename and path
    os.makedirs("downloads", exist_ok=True)
    filename = f"video_{uuid.uuid4().hex}.mp4"
    output_path = os.path.join("downloads", filename)

    ydl_opts = {
        'outtmpl': output_path,
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4'
    }

    try:
        print(f"Downloading: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Saved to: {output_path}")
        return send_file(output_path, as_attachment=True, mimetype='video/mp4')
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
