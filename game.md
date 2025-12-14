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
		<a href="{{ site.baseurl }}/game" class="nav-link active">Interactive</a>
		<a href="{{ site.baseurl }}/Beatrice" class="nav-link">Beatrice</a>
		<a href="{{ site.baseurl }}/Cyriac" class="nav-link">Cyriac</a>
		<a href="{{ site.baseurl }}/Lucas" class="nav-link">Lucas</a>
		<a href="{{ site.baseurl }}/Alexis" class="nav-link">Alexis</a>
		<a href="{{ site.github.repository_url }}" class="nav-link" target="_blank">Repository</a>
    </div>
</div>

# Fed Rate Impact Game

you can see here the game : 

<br>

<!-- --------------------------------------------------------------------------------------- -->

<!-- html of the game  -->

<div id="game-container">
  <div id="character-container">
    <img src="assets/img/game/recruiter.png" alt="Character" id="character"> <!-- for the interviewer icon -->
  </div>
  <div id="question-container">
    <p id="question-text"></p>
    <div id="answers">
      <button id="answer1" onclick="choose(0)"></button>
      <button id="answer2" onclick="choose(1)"></button>
    </div>
  </div>
</div>


<!-- --------------------------------------------------------------------------------------- -->

<!-- style of the game  -->

<style>
.game-container {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  max-width: 600px;
  margin: 50px auto;
  font-family: Arial, sans-serif;
}

.character-container img {
  width: 100px;
}

.question-container {
  background: #f0f0f0;
  padding: 20px;
  border-radius: 10px;
  flex-grow: 1;
}

.answers button {
  display: block;
  margin: 10px 0;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  background-color: #007bff;
  color: white;
}

.answers button:hover {
  background-color: #0056b3;
}
</style>


<!-- --------------------------------------------------------------------------------------- -->

<!-- script of the game -->

<script>
const questionTree = {
  text: "Welcome to your finance interview! Are you ready?",
  answers: ["Yes, let's start!", "No, maybe later."],
  next: [
    {
      text: "First question: What is a stock?",
      answers: ["A share of ownership in a company", "A type of loan"],
      next: [
        {
          text: "Correct! Next: What's ROI?",
          answers: ["Return on Investment", "Rate of Interest"],
          next: [
            { text: "Well done! You finish the interview.", answers: [], next: [] },
            { text: "Not quite. ROI is Return on Investment.", answers: [], next: [] }
          ]
        },
        {
          text: "Incorrect. A stock is a share of ownership.",
          answers: [],
          next: []
        }
      ]
    },
    {
      text: "Okay, come back later!",
      answers: [],
      next: []
    }
  ]
};

let currentNode = questionTree;

function updateQuestion() {
  document.getElementById('question-text').innerText = currentNode.text;
  
  const buttons = document.querySelectorAll('#answers button');
  buttons.forEach((btn, i) => {
    if(currentNode.answers[i]) {
      btn.style.display = "block";
      btn.innerText = currentNode.answers[i];
    } else {
      btn.style.display = "none";
    }
  });
}

function choose(index) {
  if(currentNode.next[index]) {
    currentNode = currentNode.next[index];
    updateQuestion();
  }
}

updateQuestion();
</script>

