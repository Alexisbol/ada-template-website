---
layout: default
title: Fed Rate Impact Game
permalink: /game/
---

<style>
/* Top navigation bar */
.top-nav {
    background: #000;
    border-bottom: 1px solid #333;
    position: relative;
    left: -90px;
    width: calc(100% + 180px);
    padding: 0;
    margin-bottom: 30px;
}
.top-nav-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 40px;
    display: flex;
    gap: 32px;
    align-items: center;
}
.nav-link {
    color: #999;
    text-decoration: none;
    font-size: 14px;
    font-weight: 500;
    padding: 14px 0;
    display: inline-block;
    border-bottom: 2px solid transparent;
    transition: all 0.2s ease;
}
.nav-link:hover {
    color: #fff;
    border-bottom-color: #fff;
}
.nav-link.active {
    color: #fff;
    border-bottom-color: #fff;
}
</style>

<div class="top-nav">
    <div class="top-nav-content">
        <a href="{{ site.baseurl }}/" class="nav-link">Home</a>
		<a href="{{ site.baseurl }}/other_page" class="nav-link">Analysis</a>
		<a href="{{ site.baseurl }}/game" class="nav-link active">Game</a>
		<a href="{{ site.baseurl }}/Beatrice" class="nav-link">Beatrice</a>
		<a href="{{ site.baseurl }}/Cyriac" class="nav-link">Cyriac</a>
		<a href="{{ site.baseurl }}/Lucas" class="nav-link">Lucas</a>
		<a href="{{ site.baseurl }}/Alexis" class="nav-link">Alexis</a>
		<a href="{{ site.github.repository_url }}" class="nav-link" target="_blank">Repository</a>
    </div>
</div>

# Fed Rate Impact Game


<br>

<!-- template of the game -->

<!-- --------------------------------------------------------------------------------------- -->

<!-- html of the game  -->

<div id="game-container">
  <div id="character-container">
   <!-- for theinterviewer icon (this one is free of license) -->
   <img src="{{ site.baseurl }}/assets/img/game/recruiter.png" alt="Character" id="character"> 
	<div id="question-container">
	 <p id="question-text"></p>
	 <div id="answers">
	 <button id="answer1" onclick="choose(0)"></button>
	 <button id="answer2" onclick="choose(1)"></button>
	</div>
   </div>
  </div>
</div>


<!-- --------------------------------------------------------------------------------------- -->

<!-- style of the game  -->

<style>

#game-container {
  display: flex;
  justify-content: center;
  margin: 0px auto 50px auto;
  font-family: Arial, sans-serif;
}

#character-container {
  position: relative;
  width: 600px;
}

#character-container img {
  width: 100%;
  border-radius: 10px;
}

#question-container {
  position: absolute;
  top: 60%;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(235, 235, 235, 0.9);
  padding: 15px 25px;
  width: 80%;
  border-radius: 15px;
  max-width: 650px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
  text-align: center;
}

#question-container p#question-text {
    font-size: 2em;        
    font-family: "Georgia", serif; 
    margin: 0;             
}

#answers {
  display: flex;
  justify-content: space-between; /* side by side */
  margin-top: 15px;
  gap: 10px;
}

#answers button {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1em;
  background-color: #408ad8ff;
  color: white;
  transition: background 0.2s ease;
}

#answers button:hover {
  background-color: #2c619aff;
}

</style>


<!-- --------------------------------------------------------------------------------------- -->

<!-- script of the game -->

<script>
  const questions = [
    // example of a question
  {
    text: "Welcome to your finance interview! Are you ready?", // question
    answers: ["Yes, let's start!", "No, maybe later."], // answers
    comments: ["Great! Let's begin.", "Come back when ready."] // comments for each answers
  },
  {
    text: "First question: What is a stock?",
    answers: ["A share of ownership in a company", "A type of loan"],
    comments: ["Correct!", "Incorrect. A stock is a share of ownership."]
  },
  {
    text: "What's ROI?",
    answers: ["Return on Investment", "Rate of Interest"],
    comments: ["Well done! ROI is Return on Investment.", "Not quite. ROI is Return on Investment."]
  },
  // if you want an ending where the game displays an end message here it is : 
  {
    text: "The end",
    answers: [],
    comments: []
  }
];

let currentIndex = 0;
let waitingForComment = false;
let lastAnswerIndex = null;

function updateBubble() {
  const q = questions[currentIndex];
  const questionText = document.getElementById('question-text');
  const buttons = document.querySelectorAll('#answers button');

  if (!waitingForComment) {
    questionText.innerText = q.text;
    buttons.forEach((btn, i) => {
      if (q.answers[i]) {
        btn.style.display = "block";
        btn.innerText = q.answers[i];
        btn.onclick = () => showComment(i);
      } else {
        btn.style.display = "none";
      }
    });
  } else {
    questionText.innerText = q.comments[lastAnswerIndex];
    buttons.forEach((btn, i) => {
      if (i === 0) {
        btn.style.display = "block";
        btn.innerText = "Next";
        btn.onclick = () => nextQuestion();
      } else {
        btn.style.display = "none";
      }
    });
  }
}

function showComment(answerIndex) {
  lastAnswerIndex = answerIndex;
  waitingForComment = true;
  updateBubble();
}

function nextQuestion() {
  currentIndex++;
  waitingForComment = false;
  if (currentIndex < questions.length) {
    updateBubble();
  } else {
    document.getElementById('question-text').innerText = "You've completed the game!";
    document.getElementById('answers').style.display = "none";
  }
}

updateBubble();

</script>

