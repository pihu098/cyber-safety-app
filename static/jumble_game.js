function submitWord() {
    let answer = document.getElementById("answerBox").value;

    fetch("/jumble/submit", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({answer: answer})
    })
    .then(res => res.json())
    .then(data => {

        if (data.result === "correct") {
            document.getElementById("status").innerText = "🎉 Correct! Next Level";
            setTimeout(() => location.reload(), 1000);
        }

        else if (data.result === "partial") {
            document.getElementById("status").innerText =
                data.left + " word left 🔥";
        }

        else if (data.result === "wrong") {
            document.getElementById("status").innerText =
                "❌ Wrong! Lives left: " + data.lives;
        }

        else if (data.result === "gameover") {
            document.body.innerHTML = "<h1>💀 You Lost! Try Again</h1>";
        }

    });
}


function quitGame() {
    fetch("/jumble/quit")
    .then(res => res.json())
    .then(data => {

        document.body.innerHTML =
        "<h2>🚪 You Quit Game</h2>" +
        "<h3>Answers were:</h3>" +
        "<p>" + data.answers.join(", ") + "</p>" +
        "<button onclick='location.reload()'>Next Level</button>";
    });
}
