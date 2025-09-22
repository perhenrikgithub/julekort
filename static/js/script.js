// Make sure GSAP is loaded
gsap.registerPlugin(CSSRulePlugin);

let flap = document.querySelector(".flap");
let letter = document.querySelector(".letter");
let envelope = document.querySelector(".envelope");
let shadow = document.querySelector(".shadow");

// Timeline for flap + letter animation
let t1 = gsap.timeline({ paused: true });

t1.to(flap, {
    duration: 0.75,
    rotateX: -180, // flap flips up
    transformOrigin: "top",
    ease: "power2.inOut",
})
    .set(flap, {
        zIndex: 10,
    })
    .to(letter, {
        translateY: -500,
        duration: 1.5,
        ease: "back.inOut(1)",
    })
    .set(letter, {
        zIndex: 40,
    })
    .to(letter, {
        translateY: -5,
        translateZ: 250,
        duration: 1.3,
        ease: "back.out(0.4)",
    })
    .to(flap, {
        opacity: 0,
        duration: 0.75,
    })
    .to(envelope, {
        opacity: 0,
    });

// Timeline for shadow
let t2 = gsap.timeline({ paused: true });
t2.to(shadow, {
    delay: 1.4,
    width: 450,
    boxShadow: "-75px 150px 10px 5px #eeeef3",
    duration: 0.7,
    ease: "back.out(0.2)",
});

// Function to open the card
function openCard() {
    t1.play();
    t2.play();
}

function closeCard() {
    t1.reverse();
    t2.reverse();
}

function update_helpertext(new_text) {
    let helpertext = document.getElementById("helper-text");
    helpertext.style.animation = "fadeOut 0.5s forwards";

    setTimeout(() => {
        helpertext.innerHTML = new_text;
        helpertext.style.animation = "fadeIn 2.5s forwards";
    }, 500);
}
