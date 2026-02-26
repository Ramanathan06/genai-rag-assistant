async function uploadFile() {
    const fileInput = document.getElementById("fileInput");
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    await fetch("/upload", {
        method: "POST",
        body: formData
    });

    alert("Uploaded!");
}

async function sendMessage() {
    const question = document.getElementById("question").value;

    const response = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({question})
    });

    const data = await response.json();

    const chatBox = document.getElementById("chatBox");
    chatBox.innerHTML += `<p><b>You:</b> ${question}</p>`;
    chatBox.innerHTML += `<p><b>Bot:</b> ${data.answer}</p>`;
}
