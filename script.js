document.addEventListener('DOMContentLoaded', () => {
    const botaoAudio = document.getElementById('baixar-audio');
    const botaoVideo = document.getElementById('baixar-video');
    const input = document.getElementById('url');
    const progresso = document.getElementById('progresso');

    function baixar(tipo) {
        const url = input.value;
        progresso.textContent = 'Iniciando download...';

        fetch('/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url, tipo })
        })
        .then(response => response.json())
        .then(data => {
            if (data.mensagem) {
                progresso.textContent = data.mensagem;
            } else if (data.erro) {
                progresso.textContent = "Erro: " + data.erro;
            }
        })
        .catch(error => {
            progresso.textContent = "Erro inesperado: " + error;
        });
    }

    botaoAudio.addEventListener('click', () => baixar('audio'));
    botaoVideo.addEventListener('click', () => baixar('video'));
});
