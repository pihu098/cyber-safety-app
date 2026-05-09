function playSound(id){

    let sound = document.getElementById(id);

    if(sound){

        sound.pause();

        sound.currentTime = 0;

        sound.play();

    }

}



function stopAllSounds(){

    let sounds = document.querySelectorAll("audio");

    sounds.forEach(sound => {

        sound.pause();

        sound.currentTime = 0;

    });

}



function submitWord() {

    let answer = document.getElementById("answerBox").value;

    fetch("/jumble/submit", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify({

            answer: answer

        })

    })

    .then(res => res.json())

    .then(data => {

        // ✅ CORRECT WORD
        if (data.result === "correct") {

            playSound("correctSound");

            document.getElementById("status").innerText =
                "🎉 Correct! Next Level";

            setTimeout(() => {

                location.reload();

            }, 1200);

        }

        // ✅ SOME WORDS LEFT
        else if (data.result === "partial") {

            playSound("correctSound");

            document.getElementById("status").innerText =
                "🔥 " + data.left + " word left";

        }

        // ❌ WRONG ANSWER
        else if (data.result === "wrong") {

            playSound("wrongSound");

            document.getElementById("status").innerText =
                "❌ Wrong! Lives left: " + data.lives;

        }

        // 💀 GAME OVER
        else if (data.result === "gameover") {

            playSound("loseSound");

            document.body.innerHTML = `

                <div style="text-align:center;margin-top:100px;">

                    <h1 style="color:red;">💀 Better Luck Next Time</h1>

                    <button onclick="restartGame()"
                    style="
                        padding:15px 30px;
                        border:none;
                        border-radius:10px;
                        background:#ff9800;
                        color:white;
                        font-size:20px;
                        cursor:pointer;
                    ">
                        🔄 Restart
                    </button>

                </div>

            `;

        }

    });

}



function restartGame(){

    stopAllSounds();

    window.location.href = "/jumble/restart";

}



function quitGame() {

    fetch("/jumble/quit")

    .then(res => res.json())

    .then(data => {

        playSound("loseSound");

        document.body.innerHTML = `

            <div style="text-align:center;margin-top:50px;">

                <h2>🚪 You Quit Game</h2>

                <h3>Answers were:</h3>

                <p style="font-size:25px;">
                    ${data.answers.join(", ")}
                </p>

                <button onclick="nextLevel()"
                style="
                    padding:15px 30px;
                    border:none;
                    border-radius:10px;
                    background:#4CAF50;
                    color:white;
                    font-size:20px;
                    cursor:pointer;
                ">
                    ▶ Next Level
                </button>

            </div>

        `;

    });

}



function nextLevel(){

    stopAllSounds();

    location.reload();

}



// 💡 HINT SOUND
function useHint(){

    playSound("hintSound");

}
