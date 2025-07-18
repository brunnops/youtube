from flask import Flask, render_template, request, jsonify
from pytube import YouTube
import os
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    tipo = data.get('tipo')

    try:
        yt = YouTube(url)
        titulo = yt.title.replace(" ", "_").replace("/", "_")

        if tipo == 'audio':
            stream = yt.streams.filter(only_audio=True).first()
            filename = f"{titulo}.mp4"
            output_path = stream.download(filename=filename)

            converted = f"{titulo}.mp3"
            subprocess.run(['ffmpeg', '-i', output_path, converted])
            os.remove(output_path)
            return jsonify({'mensagem': 'Áudio baixado com sucesso!'})

        elif tipo == 'video':
            stream = yt.streams.get_highest_resolution()
            filename = f"{titulo}.mp4"
            stream.download(filename=filename)
            return jsonify({'mensagem': 'Vídeo baixado com sucesso!'})

        else:
            return jsonify({'erro': 'Tipo inválido'}), 400

    except Exception as e:
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
