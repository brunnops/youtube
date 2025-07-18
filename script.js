function baixar(tipo) {
    const url = document.getElementById("url").value;
    const status = document.getElementById("status");

    if (!url) {
        status.innerText = "Por favor, insira uma URL.";
        return;
    }

    status.innerText = "Iniciando download...";

    fetch("/baixar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url, tipo })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "sucesso") {
            status.innerText = `Download concluído: ${data.arquivo}`;
        } else {
            status.innerText = "Erro: " + data.mensagem;
        }
    })
    .catch(err => {
        status.innerText = "Erro: " + err.message;
    });
}
