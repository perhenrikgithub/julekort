textarea = document.getElementById("card_text");
textarea.addEventListener("input", (event) => {
    document.getElementById("card_text_preview").innerText = event.target.value;

    let lines = textarea.value.split("\n");

    // Limit characters per line
    lines = lines.map((line) => line.slice(0, maxCharsPerLine));

    // Limit number of lines
    if (lines.length > maxLines) {
        lines = lines.slice(0, maxLines);
    }

    textarea.value = lines.join("\n");
});
