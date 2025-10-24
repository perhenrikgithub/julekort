const div = document.getElementById("story-teller");
const buttons = document.querySelectorAll(".options > button");

const sentences = [
    { text: "Julekort er gøy!", fontSize: "6em", show_for: 3000 },
    { text: "Det er koselig å sende julekort.", fontSize: "6em", show_for: 3000 },
    { text: "Det er koselig å få julekort.", fontSize: "6em", show_for: 3000 },
    { text: "Men dyrt å sende til hele verden.", fontSize: "6em", show_for: 4000 },
    { text: "Julepost 2025", fontSize: "6em", show_for: 3000 },
];

let currentIndex = 0;
let isSkipped = false;

function showNextSentence() {
    if (isSkipped || currentIndex >= sentences.length) {
        // Skip to the last sentence
        const last = sentences[sentences.length - 1];
        div.innerText = last.text;
        div.style.fontSize = last.fontSize;
        div.style.transition = "none";
        div.style.opacity = "1";
        showButtons();
        return;
    }

    const sentence = sentences[currentIndex];

    // Fade out
    div.style.transition = "opacity 2s";
    div.style.opacity = "0";

    setTimeout(() => {
        if (isSkipped) {
            showNextSentence();
            return;
        }

        // Fade in
        div.innerText = sentence.text;
        div.style.fontSize = sentence.fontSize;
        div.style.transition = "opacity 2s";
        div.style.opacity = "1";

        // Schedule next sentence
        currentIndex++;
        setTimeout(showNextSentence, sentence.show_for);
    }, 2000);
}

function showButtons() {
    buttons.forEach((btn) => {
        btn.style.transition = "opacity 1s";
        btn.style.opacity = "1";
    });
}

function skipStory() {
    isSkipped = true;
    showNextSentence();
}

showNextSentence();
