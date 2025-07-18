function baixar() {
    const url = document.getElementById('url').value;
    const tipo = document.getElementById('tipo').value;

    const form = new FormData();
    form.append('url', url);
    form.append('tipo', tipo);

    fetch('/download', {
        method: 'POST',
        body: form
    })
    .then(response => response.blob())
    .then(blob => {
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = tipo === 'audio' ? 'audio.mp4' : 'video.mp4';
        link.click();
    });
}
