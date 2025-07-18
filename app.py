from flask import Flask, render_template, request, jsonify
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/baixar', methods=['POST'])
def baixar():
    data = request.json
    url = data.get('url')
    tipo = data.get('tipo')  # 'audio' ou 'video'

    try:
        yt = YouTube(url)
        if tipo == 'audio':
            stream = yt.streams.filter(only_audio=True).first()
            nome_arquivo = yt.title + ".mp3"
        else:
            stream = yt.streams.get_highest_resolution()
            nome_arquivo = yt.title + ".mp4"

        stream.download(filename=nome_arquivo)
        return jsonify({'status': 'sucesso', 'arquivo': nome_arquivo})
    except Exception as e:
        return jsonify({'status': 'erro', 'mensagem': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
