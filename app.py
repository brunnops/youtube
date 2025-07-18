from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    tipo = request.form['tipo']
    
    yt = YouTube(url)

    if tipo == 'audio':
        stream = yt.streams.filter(only_audio=True).first()
        filename = 'audio.mp4'
    else:
        stream = yt.streams.get_highest_resolution()
        filename = 'video.mp4'

    stream.download(filename=filename)
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
