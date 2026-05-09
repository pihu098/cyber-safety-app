function playSound(id){

    let sound = document.getElementById(id);

    sound.pause();

    sound.currentTime = 0;

    sound.play();

}



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

function playWinSound(){

    let sound = document.getElementById("winSound");

    sound.pause();

    sound.currentTime = 0;

    sound.play();

}

function playLoseSound(){

    let sound = document.getElementById("loseSound");

    sound.pause();

    sound.currentTime = 0;

    sound.play();

}


function stopSounds(){

    document.getElementById("winSound").pause();

    document.getElementById("loseSound").pause();

}


function checkAnswer(selected){

    fetch("/check_answer",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            answer:selected
        })

    })

    .then(res => res.json())

    .then(data => {

        if(data.correct){

            playWinSound();

            setTimeout(()=>{

                alert("🎉 YOU WON");

                stopSounds();

                location.reload();

            },1000);

        }

        else if(data.gameover){

            playLoseSound();

            setTimeout(()=>{

                alert("💀 Better Luck Next Time");

                stopSounds();

                location.reload();

            },1000);

        }

        else{

            playLoseSound();

            alert("❌ Wrong Answer");

        }

    });

}
