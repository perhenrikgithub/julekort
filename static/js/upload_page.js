// max file size frontend validation
const allowedTypes = ["image/jpeg", "image/png"];
const maxFileSize = 1 * 1024 * 1024; // 1 MB
document.getElementById("card_image").addEventListener("change", function (e) {
    if (e.target.files[0] && e.target.files[0].size > maxFileSize) {
        alert("Å nei! Filen er for stor for julenissens slede! (maks " + maxFileSize / 1024 / 1024 + "MB).");
        e.target.value = "";
    }
});

// Card text preview and limits
const maxCharsPerLine = 38;
const maxLines = 14;

const cardTextArea = document.getElementById("card_text");
const preview = document.getElementById("card_text_preview");

function updateCardTextPreview() {
    let lines = cardTextArea.value.split("\n");
    preview.innerText = lines.join("\n");
}

cardTextArea.addEventListener("input", () => {
    updateCardTextPreview();
});

updateCardTextPreview();
