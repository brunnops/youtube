function baixar(tipo) {
  const url = document.getElementById("url").value;
  const progress = document.getElementById("progress");
  if (!url) return alert("Por favor, insira uma URL.");

  progress.style.display = 'block';

  fetch("/download", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ url: url, tipo: tipo })
  })
  .then(response => {
    if (!response.ok) throw new Error("Erro ao baixar o arquivo");
    return response.blob();
  })
  .then(blob => {
    const link = document.createElement("a");
    link.href = window.URL.createObjectURL(blob);
    link.download = tipo === "audio" ? "audio.mp3" : "video.mp4";
    document.body.appendChild(link);
    link.click();
    link.remove();
  })
  .catch(error => {
    alert("Erro: " + error.message);
  })
  .finally(() => {
    progress.style.display = 'none';
  });
}
