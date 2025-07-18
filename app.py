from flask import Flask, request, send_file, jsonify
from yt_dlp import YoutubeDL
import os
import tempfile
import uuid

app = Flask(__name__)

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url")
    tipo = data.get("tipo")  # "audio" ou "video"

    if not url or tipo not in ["audio", "video"]:
        return jsonify({"error": "Requisição inválida"}), 400

    try:
        temp_dir = tempfile.mkdtemp()
        output_template = os.path.join(temp_dir, f"%(title)s-{uuid.uuid4().hex}.%(ext)s")

        if tipo == "audio":
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": output_template,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
                "ffmpeg_location": "ffmpeg.exe"
            }
        else:  # vídeo
            ydl_opts = {
                "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "merge_output_format": "mp4",
                "outtmpl": output_template,
                "ffmpeg_location": "ffmpeg.exe"
            }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if tipo == "audio":
                filename = os.path.splitext(filename)[0] + ".mp3"

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
