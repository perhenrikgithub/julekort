// max file size frontend validation
const allowedTypes = ["image/jpeg", "image/png"];
const maxFileSize = 1 * 1024 * 1024; // 1 MB
const imageInput = document.getElementById("card_image");
imageInput.addEventListener("change", function (e) {
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

// removal of file input field if image_url saved as cookie
const imageUrl = document.cookie
    .split("; ")
    .find((row) => row.startsWith("image_url="))
    ?.split("=")[1];

let lastRecipient = decodeURIComponent(
    document.cookie
        .split("; ")
        .find((row) => row.startsWith("recipient="))
        ?.split("=")[1] || ""
);

// Fjern oktale escapes som \054 og erstatt med faktisk komma
lastRecipient = lastRecipient.replace(/\\054/g, ",");
lastRecipient = lastRecipient.replace('"', "");
lastRecipient = lastRecipient.replace('"', "");

if (lastRecipient.includes(",")) {
    const recipients = lastRecipient.split(",");
    lastRecipient = recipients.map((r) => r.trim()).join("\n");
    console.log("multiple recipients", lastRecipient);
}

if (imageUrl) {
    imageInput.style.display = "none";
    const cardImageLabel = document.getElementById("card_image_label");
    cardImageLabel.style.display = "none";
    const fileInputInfo = document.getElementById("file_input_info");
    const removeFileButton = document.getElementById("remove_file_button");
    removeFileButton.style.display = "inline";
    removeFileButton.addEventListener("click", () => {
        imageInput.value = "";
        imageInput.style.display = "block";
        cardImageLabel.style.display = "block";
        fileInputInfo.style.display = "none";
        removeFileButton.style.display = "none";
        document.getElementById("image_url").value = "";
        // remove cookie
        document.cookie = "image_url=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        document.cookie = "recipient=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    });
    fileInputInfo.innerText = "Julenissen har en kopi av bilde \ndu sendte inn sist til: \n" + lastRecipient;
    fileInputInfo.style.display = "block";
}
