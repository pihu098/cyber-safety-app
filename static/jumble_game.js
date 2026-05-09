let currentWord = "";

// 🔊 PLAY SOUND
function playSound(id){

    let sound = document.getElementById(id);

    if(sound){

        sound.currentTime = 0;

        sound.play()
        .catch(err => console.log(err));

    }

}

// 🔴 STOP ALL SOUNDS
function stopAllSounds(){

    let sounds = document.querySelectorAll("audio");

    sounds.forEach(sound => {

        sound.pause();

        sound.currentTime = 0;

    });

}

// 🟨 PICK LETTER
function pick(letter){

    currentWord += letter;

    document.getElementById("answer").innerHTML = currentWord;

    document.getElementById("wordInput").value = currentWord;

}

// ❌ CLEAR
function clearWord(){

    currentWord = "";

    document.getElementById("answer").innerHTML = "";

    document.getElementById("wordInput").value = "";

}

// ✅ SUBMIT WORD
function submitWord(){

    let word = document.getElementById("wordInput").value;

    fetch("/jumble/check",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            answer:word
        })

    })

    .then(r=>r.json())

    .then(data=>{

        // ✅ CORRECT WORD
        if(data.result=="correct"){

            playSound("correctSound");

            document.getElementById("foundWords").innerHTML +=
            "✅ " + word + "<br>";

            document.getElementById("count").innerHTML =
            data.found.length;

            document.getElementById("coins").innerHTML =
            data.coins;

            clearWord();

        }

        // 🎉 ALL WORDS FOUND
        else if(data.result=="win"){

            playSound("winSound");

            document.getElementById("result").innerHTML =

            "<div class='win'>🎉 YOU WON 🎉</div><br>" +

            "<button onclick='nextLevel()'>CHAPTER NEXT ➜</button>";

        }

        // ❌ WRONG
        else if(data.result=="wrong"){

            playSound("wrongSound");

            alert("❌ Wrong Word");

        }

        // 💀 GAME OVER
        else if(data.result=="gameover"){

            playSound("loseSound");

            alert("💀 Better Luck Next Time");

            window.location="/jumble/restart";

        }

    });

}

// 💡 HINT
function getHint(){

    playSound("hintSound");

    fetch("/jumble/hint")

    .then(r=>r.json())

    .then(data=>{

        if(data.hint){

            alert("💡 Hint: " + data.hint);

            document.getElementById("coins").innerHTML =
            data.coins;

        }

        else{

            alert(data.error);

        }

    });

}

// ▶ NEXT LEVEL
function nextLevel(){

    stopAllSounds();

    window.location="/jumble";

}


window.onload = function(){

    document.getElementById("submitBtn")
    .addEventListener("click", submitWord);

    document.getElementById("clearBtn")
    .addEventListener("click", clearWord);

    document.getElementById("hintBtn")
    .addEventListener("click", getHint);

}
