---
layout: default
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
        <a href="{{ site.baseurl }}/game" class="nav-link">Game</a>
        <a href="{{ site.baseurl }}/Beatrice" class="nav-link">Beatrice</a>
        <a href="{{ site.baseurl }}/Cyriac" class="nav-link">Cyriac</a>
        <a href="{{ site.baseurl }}/Lucas" class="nav-link active">Lucas</a>
        <a href="{{ site.baseurl }}/Alexis" class="nav-link">Alexis</a>
        <a href="{{ site.github.repository_url }}" class="nav-link" target="_blank">Repository</a>
    </div>
</div>




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
    text: "Do you think that two companies with comparable results on a given period will necesseraly react the same to fed events ?", // question
    answers: ["Yes, they have similar results", "No, not necesseraly"], // answers
    comments: ["Not quite. Similar results doesn't tell the full story on the strategies of the companies and how they will behave in a different situation", "Indeed ! same results for a period of time cannot guarantee similar behavior given a different situation"] // comments for each answers
  },
    {
    text: "To assess similarity of results of two companies, is it sufficient to look only at the Volume of shares or only at the Price of the shares",
    answers: ["Yes, we can assess with only one", "No, we would need both"],
    comments: ["Incorrect. It is hard to assess by considering only one dimension of the company, either physical or financial. We need to combine both to get real insight on the performance of a company", "Precisely ! Only by combining both can we get real insight on the performance of a company"]
  },
  // if you want an ending where the game displays an end message here it is : 
  {
    text: "Let us have a better look at how to answer these questions in practice",
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

<br>
<br>
<br>


Like you just saw, one of the questions we can ask ourselves is what the impact of fed rates on two comparable companies, given a comparison criterion, can reveal on the specifics of the companies. The idea is to study the reactions and reactivities to fed rates events and link different reactions to different underlying truths about the companies, their functionning and economic strategies.


## Idea behing the Analysis

A relevant analysis of the impact of the fed rates asks for a relevant difference in the behavior of the two companies we are focusing on. The idea behind your work therefore needs to lie in defining a comparability measure to indentify pairs of companies both strongly comparable before the event, and significantly different after.

 
## Comparability Methods 

A first comment goes towards the sectors of the companies. To achieve a more relevant analysis, you need to only consider pairs of companies from within the same sector. This way the results cannot be biased by between-sectors difference in behaviors. The rest of the approach of comparability is based on the features of the companies.

A first obstacle in the definition of a comparabilty measure lies in the volatility of these features along a time period.
The solution you should adopt is thus to think of a local measure of how similar two companies are on a given small time period. This approach fits the question as you only aim to study the impact of localized fed rate events, hence the evolution of the before and after the event for two companies. The idea is then to define a small time window on which you can compare the values of a given feature for both companies.

The issue that arises with this method, and second obstacle, is to account for outliers, meaning localized behaviors of the features that are not inscribed in the global trend of the window. As the idea is to ultimaetely define a similarity metric (a number), the idea that you can come up with to nullify the impact of these outliers in theory is to consider the median of the values that the feature takes. Like we said, This approach has the advantage to limit the influence of the outliers when summarizing the behavior of the feature, in opposition to a mean that would be highly reactive to the formers.

A Third obstacle lies in the fact that you are so far comparing raw values, without considering the scales of the features. In fact, when dealing with objects that come in a vast diversity like companies, it is important to account for their scale, because what can be a huge change in raw numbers can also turn out to be a minor event in the eye of an even bigger company. In that sense, a raw numbers approach would discard any pairs of large scale companies during the sorting. A solution that you could adopt is to consider the Bray-Curtis dissimalirity which brings back a difference in raw numbers to the scale of the numbers themselves. 

Once all these obstacles have been tackled you end up with the complete method for comparing two companies, which can be summarized in the following equation 

> 
>  <img src="assets/img/Lucas/comparability_measure.png" height="70em">
>
> With X̃ the median of the feature considered for the company X during the time window considered 
>


## Focus on the Features

Given the comparison method that we have derived, you have to find which feature of a company would best express this notion of comparibility. Having already taken care of the sector of the company, the idea of comparability now only lies intuitively in a notion of "size" of the company. We have already discussed this notion in the part on the size dependent analysis, but as a reminder the idea is here to compare companies of similar "size". We have defined this concept of "similar" already what is left is to look into how different features, both given by your dataset and engineered yourself, could better represent the "size" of a company.

You may first consider features like Volume of shares exchanged and Return. Now the latter is already an engineered feature, defined as the percentage of difference between two Closing prices distanced by a given time period (generally for us 21 days). But as you remember from the interview questions, the issue that arises from these features is their uncomplete economical grounding. In fact we can imagine a company that has issued a large amount of consequently cheap shares, which would imply that a large quantity of exchanged shares doesn't necesseraly represent a large amount of money exchanged. Similarly, a big difference in Closing prices in a compay with a low amount of shares issued doesn't necessarily represent an important financial gain or loss. You may have realized by now that each feature lacks what the other offers. The idea is then to combine the notions behind them into composite features that display a more complete economical grounding.

The feature created from this conclusion is called Dollar Volume and depends on a third one called Typical price. The latter is a well known feature used in finance and is defined as a weighted average of all the prices of a share (Opening, Closing, Highest, Lowest). This feature helps us to define a more adaptable and all encompassing notion of price for a company share. We then define our Dollar Volume as the product of the amount of shares traded and the typical price of a share, to get a quantifier of the amount of financial volume traded.

On a side note, we also define a feature called Dollar Return as the product between the Return and the Typical price that helps us in the analysis to better quantify the gains or losses of a company in monitary terms.


## Relevance of the Results

One key ingredient is missing to your pipeline so far... Everything mentioned combined only offers an automized way to get pairs of companies with the most interesting properties of similarity for your analysis, but it never guarantees the existence of the statistical significance of said properties. What we mean is the fact that you merely sort the pairs based on a similarity and dissimilarity score to get companies the most similar at the beginning and most different at the end of the event, but nothing in the process guarantees that these difference are statistically significant. 

A solution for you is to introduce different t-test at different steps of the pipeline to study their p values. In that sense, you can set up t-test for the evolution of the feature of the company, in order to quantify the impact on these features. For the sake of simplicity afterwards we refer to associated p values as "pvd" as in p value of the difference in the evolution of the features. In addition you can have t-test comparing both companies on the start and end windows of the event to test the significance of the start similarity and end dissimilarity mentionned previously. Again for the sake of simplicity we refer to associated p values as "pvs" for the start and "pve" for the end.

But these tests allow you to only discuss significant changes in the behavior of the companies, and not assess the role of the fed rates in those changes. A last step towards the relevance of your results is the introduction of correlations and linear regressions to study the link between these evolutions in the features of the company and the evolution of the fed rate. We refer to associated p values as "pvc" as in correlation.


## Case studies

Through the different aspects of this research question we have defined a fully functionning pipeline aiming to produce pairs of companies judged "comparable" along with the significance of this judgement. Nevertheless, the real analysis lies past this pipeline and focuses rather on its product. Here is a selection of the most relevant cases to analyse what different behaviors from comparable companies can reveal about their functionning. 

For the case studies, this pipeline is ran on the feature Dollar Volume and on a fed event linked to the 2008 crisis. In the plots all the features are cross-normalized, meaning normalized taking the maximum of both and the minimum of both. This approach allows to plot them along the fed rates while keeping their relation to each other. The fed rates however are simply normalized in a general manner. 


<style>


    .image-configurator {
    position: relative;
    flex: 2;
    aspect-ratio: 16 / 9;
    width: 100%;
    min-height: 300px;
    }


    .image-configurator img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    background: #fafafa;
    }

    .menu {
    position: relative;
    min-width: 160px;
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid #aaa;
    z-index: 10;
    text-align: center;
    border-radius: 5px;
    }

    .menu.left { left: 10px; }
    .menu.right { right: 10px; }

    .menu-header {
    padding: 6px 8px;
    cursor: pointer;
    background: #f4f4f4;
    user-select: none;
    font-weight: bold;
    border-radius: inherit;
    }

    .menu-header::after {
    content: "▼";
    float: right;
    font-size: 10px;
    }

    .menu-content {
    display: none;
    max-height: 140px;
    overflow-y: auto;
    border-top: 1px solid #aaa;
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    z-index: 50;
    border: 1px solid #aaa;
    }

   .menu-content div {
    padding: 6px 8px;
    cursor: pointer;
    border-bottom: 1px solid #ccc; 
    background: #fff; 
    }
    .menu-content div:hover {
        background: #f0f0f0; 
    }

    .menu.open .menu-content {
    display: block;
    }

    .pair-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 30px;              
    max-width: 1500px;
    margin: 0 auto;
    }

    .pair-text {
    flex: 1 1 300px;
    max-width: 300px;
    padding: 15px;
    border: 1px solid #aaa;
    background: #f9f9f9;
    font-family: Arial, sans-serif;
    line-height: 1.5;
    border-radius: 5px;
    }

    .plot-column {
    display: flex;
    flex-direction: column;
    flex: 2 1 600px;
    gap: 10px;
    }

    .menu-bar {
    display: flex;
    justify-content: flex-start;
    gap: 50px;  
    margin-bottom: 10px;
    position: relative;
    z-index 100;
    }

    #mainPlot {
    width: 100% !important;
    height: 100% !important;
    }

    @media (max-width: 900px) {
      .pair-container {
          flex-direction: column;
          align-items: center;
      }
      .plot-column, .pair-text {
          width: 100%;
      }
    }

</style>


<div class="pair-container">
    <div class="pair-text" id="pairText">
    </div>
    <div class="plot-column">
        <div class="menu-bar">
            <div class="menu left" id="categoryMenu">
                <div class="menu-header">Category</div>
                <div class="menu-content"></div>
            </div>
            <div class="menu right" id="imageMenu">
                <div class="menu-header">Feature</div>
                <div class="menu-content"></div>
            </div>
        </div>
        <div class="image-configurator">
            <div id="mainPlot"></div>
        </div>
    </div>
</div>



<script src="https://cdn.plot.ly/plotly-2.30.0.min.js"></script>

<script>
const pairs = {
  "ARAY vs DVA": {
    json: "{{ site.baseurl }}/data/(ARAY,DVA).json",
    description: `<b> ARAY vs DVA — Healthcare sector </b> 
    <br> 
    <br> <i>Accuracy Inc</i> 
    <br>( pvd : 0.037 ) ( pvc : 0.008 )
    <br> <i>Davita Inc</i> 
    <br>( pvd : 0.037 ) ( pvc : 0.314 )
    <br> 
    <br> pvs : 0.883
    <br> pve : 0.002 
    <br> 
    <br> We can see a sustained drop in dollar return for ARAY and a sharp increase in dollar volume for DVA
    <br> 
    <br>
    <br> <b> ARAY is a biotech company with important research stages that rely on financing. DVA on the other hand mainly provides dialysis services, which are a more stable source of income often tied to insurance reimbursements </b>` 
  },

  "AGX vs ARTW": {
    json: "{{ site.baseurl }}/data/(AGX,ARTW).json",
    description: ` <b> AGX vs ARTW — Industry sector </b>
    <br> 
    <br> <i>Argan Inc</i> 
    <br>( pvd : 0.014 ) ( pvc : 0.912)
    <br> <i>Art’s Way Manufacturing Co Inc</i> 
    <br>( pvd : 0.165 ) (pvc : 0.0)
    <br> 
    <br> pvs : 0.999 
    <br> pve : 0.089 
    <br> 
    <br> We can see an increase in dollar return for AGX and a shaper increase in dollar volume for ARTW
    <br> 
    <br>
    <br> <b> AGX is a construction and industrial services firm which operates by providing services in related fields. ARTW is a smaller industrial equipment manufacturer specialized, in particular, in agricultural machinery  </b>` 
  },

  "ASTC vs ALOT": {
    json: "{{ site.baseurl }}/data/(ASTC,ALOT).json",
    description: ` <b> ASTC vs ALOT — Technology sector </b>
    <br> 
    <br> <i>Astrotech Corp</i> 
    <br>( pvd : 0.016 ) ( pvc : 0.0)
    <br> <i>AstraNova Inc</i> 
    <br>( pvd : 0.964 ) (pvc : 0.512)
    <br> 
    <br> pvs : 0.456 
    <br> pve : 0.009 
    <br> 
    <br> We can see an increase in dollar return and in dollar volume for ASTC 
    <br> 
    <br>
    <br> <b> ASTC is a small company, heavily development-oriented focused on spectrometry and the commercialization of detection technologies. ALOT is a larger and more established company, which focuses on the manifacture of technologies such as aerospace printing hardware </b>` 
  },

  "DVN vs MUR": {
    json: "{{ site.baseurl }}/data/(DVN,MUR).json",
    description: ` <b> DVN vs MUR — Energy sector </b> 
    <br> 
    <br> <i>Devon Energy Corp</i> 
    <br>( pvd : 0.005 ) ( pvc : 0.028)
    <br> <i>Murphy Oil Corp</i> 
    <br>( pvd : 0.975 ) (pvc : 0.5)
    <br> 
    <br> pvs : 0.0 
    <br> pve : 0.0 
    <br> 
    <br> We can see an increase in dollar return more important for DVN and an increase in dollar volume for DVN
    <br> 
    <br>
    <br> <b> DVN and MUR are both upstream oil and gas producers. DVN aims for rapid expansion throught exploration and acquisition of geographical sites and development of new fields, while MUR operates with careful geographic diversification </b>` 
  }
};

const categoryMenu = document.getElementById("categoryMenu");
const imageMenu = document.getElementById("imageMenu");
const categoryContent = categoryMenu.querySelector(".menu-content");
const imageContent = imageMenu.querySelector(".menu-content");
const pairText = document.getElementById("pairText");

let currentPairLabel = Object.keys(pairs)[0];
let currentFeature = null;
let currentJSON = null;

async function loadJSON(path) {
  const res = await fetch(path);
  return await res.json();
}

function fedEventShape(json) {
  return {
    type: "rect",
    xref: "x",
    yref: "paper",
    x0: json.fed_event.start,
    x1: json.fed_event.end,
    y0: 0,
    y1: 1,
    fillcolor: "rgba(255,0,0,0.15)",
    line: { width: 0 }
  };
}

function plotFeature(json, feature) {
  if (!json || !feature) return;
  
  const dates = Object.keys(json.data).sort();
  const [t1, t2] = json.pair;

  const y1 = dates.map(d => json.data[d][feature][t1]);
  const y2 = dates.map(d => json.data[d][feature][t2]);
  const fedY = dates.map(d => json.data[d].Fed_rate);

  const shapes = [ fedEventShape(json) ];

  Plotly.react("mainPlot", [
    { x: dates, y: y1, mode: "lines", name: t1, line: { color: "orange" } },
    { x: dates, y: y2, mode: "lines", name: t2, line: { color: "blue" } },
    { x: dates, y: fedY, mode: "lines", name: "Fed Rate", line: { color: "green" } }
  ], {
    title: `${feature} — ${t1} vs ${t2}`,
    yaxis: { title: feature },
    shapes: shapes,
    margin: { t: 50 },
    legend: { orientation: "h" }
  });
}

function closeMenus() {
  categoryMenu.classList.remove("open");
  imageMenu.classList.remove("open");
}

function loadPairs() {
  categoryContent.innerHTML = "";

  Object.entries(pairs).forEach(([label, cfg]) => {
    const item = document.createElement("div");
    item.textContent = label;

    item.onclick = async () => {
      currentPairLabel = label;
      categoryMenu.querySelector(".menu-header").textContent = label;
      pairText.innerHTML = cfg.description;

      currentJSON = await loadJSON(cfg.json);
      loadFeatures(currentJSON);

      closeMenus();
    };

    categoryContent.appendChild(item);
  });
}

function loadFeatures(json) {
  imageContent.innerHTML = "";

  json.features.forEach((feature, i) => {
    const item = document.createElement("div");
    item.textContent = feature;

    item.onclick = () => {
      currentFeature = feature;
      imageMenu.querySelector(".menu-header").textContent = feature;
      plotFeature(json, feature);
      closeMenus();
    };

    imageContent.appendChild(item);

    // Automatically plot the first feature
    if (i === 0) {
      currentFeature = feature;
      imageMenu.querySelector(".menu-header").textContent = feature;
      plotFeature(json, feature);
    }
  });
}

categoryMenu.querySelector(".menu-header").onclick = e => {
  e.stopPropagation();
  categoryMenu.classList.toggle("open");
  imageMenu.classList.remove("open");
};

imageMenu.querySelector(".menu-header").onclick = e => {
  e.stopPropagation();
  imageMenu.classList.toggle("open");
  categoryMenu.classList.remove("open");
};

document.addEventListener("click", closeMenus);

// Initialization
(async function init() {
  loadPairs();

  const firstPair = pairs[currentPairLabel];
  categoryMenu.querySelector(".menu-header").textContent = currentPairLabel;
  pairText.innerHTML = firstPair.description;

  currentJSON = await loadJSON(firstPair.json);
  loadFeatures(currentJSON);
})();

</script>

<br>
<br>

## Results and interpretations

The case studies seem to tie a companie's resilience, that is its low reactivity to fed rates and stability, to two main component of its functionning. 

### What first seems to matter is its business model. 

In the example of the stocks ASTC and ALOT, ASTC was more responsive to fed rates, whereas ALOT was more stable. We can explain this difference of behavior by a difference of business model. In fact ASTC is more development oriented, while ALOT is only manufacturing. This implies that ASTC's revenues are not certain and depend on the financing of the research and development. In fact, when the fed rates go down, investors are more tempted to finance such projects as they do it at a lower cost for them. On the other hand, ALOT's revenues are stable as the company only sells a product on the market, whose value is more stable. 

In the example of the stocks DVN and MUR, it was DVN that was more responsive to fed rates, while MUR was also responsive but with a weaker response. This difference can be explained in their respective strategies, which can be described as respectively more aggressive and more conservative. The difference in business model, either growth-oriented or stability oriented, leads the reactivity to fed rates and increase of decrease in investments.

### A second key element is its target market and its scale

In the example of AGX and ARTW, both were responding but in different ways and to different consequences of the fed event. 
AGX was leading in terms of increase of dollar volume, which we can link to the fact that fed rate drops are tied to the incentive for wealthy actors to place their money which explodes the volume of shares of a company. In the case of AGX, it is the perfect choice for these investors as it is a large scale industrial company with large contracts and a historically good balance sheet : in other terms a safe choice. But this portfolio reallocation doesn't imply a reevaluation of the value of a share, meaning the placing is rather speculative in this case. On the other hand ARTW shows an increase in dollar return because, as a small company, it is rather value driven and not flow driven. In the context of a drop in the fed rates investors revalue the price of the share of the stock, hence the company knows a price effect which in this case increases its overall return.

<br>
<br>

This whole question gave us a good intuition on how what can first look like comparable companies, with comparable results, can have very different structure and strategies, leading to very different reactions to fed rates. That's why depending on the configuration of the market and the fed rates, not every similarly performing company is worth betting on, and a more in depth analysis of the underlying functionning of the companies is necessary to maximize the gains, or at leasts minimize the risk of losses.