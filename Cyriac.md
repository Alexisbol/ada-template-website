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
.content-section h2 {
    border-bottom: 1px solid #e0e0e0;
    padding-bottom: 0.3em;
    margin-bottom: 1em;
}
</style>

<div class="top-nav">
    <div class="top-nav-content">
        <a href="{{ site.baseurl }}/" class="nav-link">Home</a>
        <a href="{{ site.baseurl }}/other_page" class="nav-link">Analysis</a>
        <a href="{{ site.baseurl }}/game" class="nav-link">Game</a>
        <a href="{{ site.baseurl }}/Beatrice" class="nav-link">Beatrice</a>
        <a href="{{ site.baseurl }}/Cyriac" class="nav-link active">Cyriac</a>
        <a href="{{ site.baseurl }}/Lucas" class="nav-link">Lucas</a>
        <a href="{{ site.baseurl }}/Alexis" class="nav-link">Alexis</a>
        <a href="{{ site.github.repository_url }}" class="nav-link" target="_blank">Repository</a>
    </div>
</div>

## Dataset presentation

We first want to have a quick overview of the dataset, what it contains exactly and its structure. The Stock Market Dataset from kaggle, contains
historical daily prices of Nasdaq-traded stocks and ETFs. For a given stock, we have the opening price, higest daily price, lowest daily price, closing price, volume of exchanges of the stock and the adjusted closing price. We also have, acces to the sector of each stock's corresponding company, its Nasdaq ticker name and actual name. For a more visual overview and global exploration, the following tree map displays the thirty five most valuable stocks of each sector, where the value is given in avaerage dollar volume (the average value of the total daily exchanged dollars).

<div id="treemap" style="width:100%; height:600px;"></div>



The dataset does not only contain stocks, but also ETFs (Exchange-Traded Funds), which can be imagined like a grouping of stocks of the same sector. An example of this is "DBA", the Invesco DB Agriculture Fund, which groups stocks in the agricultural sector. In principle, ETF are meant to lower the investor's risk since the crash of a single stock can be counterbalanced by the remainding ones.

<div id="sunburst" style="width:100%; height:700px;"></div>




<!--<div id="question-container">
  <div id="character-container">
   <!-- for theinterviewer icon (this one is free of license) - #->
   <img src="{{ site.baseurl }}/assets/img/game/recruiter.png" alt="Character" id="character"> 
	<div id="question-container">
	 <p id="question-text">'Next, I would like to ask you: If I give you the choice between a stock of a small, medium or large company, which do you expect to be more risky to invest in, just after a positive fed rate event?'</p>
   </div>
  </div>
</div>

<style>

#question-container {
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

</style>-->
<!-- ---------------- Floating Game HTML ---------------- -->
<div id="floating-image-wrapper">
    <button id="close-game">&times;</button>
    <button id="minimize-game">–</button>
    <img id="floating-image" src="{{ site.baseurl }}/assets/img/game/recruiter.png" alt="Sticky visual"/>
    <div id="question-container">
        <p id="question-text"></p>
        <div id="answers">
            <button onclick="choose(0)"></button>
            <button onclick="choose(1)"></button>
        </div>
    </div>
</div>

<!-- ---------------- Floating Game CSS ---------------- -->
<style>
#floating-image-wrapper {
    position: fixed;
    top: 10%;
    right: 5%;
    pointer-events: none;
    z-index: 999;
    transition: all 0.6s ease;
}

#floating-image-wrapper img {
    width: 180px;
    border-radius: 10px;
    transition: all 0.6s ease;
}

/* Active state moves to center */
#floating-image-wrapper.active {
    top: 50%;
    right: 50%;
    transform: translate(50%, -50%);
    pointer-events: auto;
}

#floating-image-wrapper.active img {
    width: 70vw;
    max-width: 900px;
}

/* Question container */
#question-container {
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.6s ease;
    background: rgba(235, 235, 235, 0.95);
    padding: 15px 25px;
    width: 80%;
    max-width: 650px;
    border-radius: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    text-align: center;
    position: absolute;
    top: 60%;
    left: 50%;
    transform: translateX(-50%);
}

/* Answers */
#answers {
    display: flex;
    justify-content: space-between;
    gap: 10px;
    margin-top: 15px;
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

/* Close button inside image */
#close-game {
    position: absolute;
    top: 70%;
    right: 70%;
    background: red;
    color: white;
    font-size: 1.5em;
    border: none;
    border-radius: 50%;
    width: 35px;
    height: 35px;
    cursor: pointer;
    z-index: 1000;
    line-height: 30px;
    text-align: center;
    padding: 0;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s ease;
}

/* Minimize button top-right corner */
#minimize-game {
    position: absolute;
    top: -10px;
    right: -10px;
    background: grey;
    color: white;
    font-size: 1.5em;
    border: none;
    border-radius: 50%;
    width: 35px;
    height: 35px;
    cursor: pointer;
    z-index: 1000;
    line-height: 30px;
    text-align: center;
    padding: 0;
    pointer-events: auto;
}

/* Minimized state hides image and question (close button hidden automatically) */
#floating-image-wrapper.minimized #floating-image,
#floating-image-wrapper.minimized #question-container,
#floating-image-wrapper.minimized #close-game {
    opacity: 0;
    pointer-events: none;
}

#floating-image-wrapper.active #question-container {
    opacity: 1;
    pointer-events: auto;
}

#floating-image-wrapper.active #close-game {
    opacity: 1;
    pointer-events: auto;
}
</style>

<!-- ---------------- Floating Game JS ---------------- -->
<script>
document.addEventListener("DOMContentLoaded", () => {

    const floating = document.getElementById("floating-image-wrapper");
    const triggers = document.querySelectorAll(".trigger-game");
    const closeBtn = document.getElementById("close-game");
    const minimizeBtn = document.getElementById("minimize-game");
    const questionContainer = document.getElementById("question-container");
    const floatingImage = document.getElementById("floating-image");

    // ---------------- Multiple games ----------------
    const games = {
        "stock-size": {
            text: "Stock Size Game: Ready?",
            answers: ["Yes", "No"],
            next: [
                {
                    text: "Which stock size is riskier after a positive fed rate?",
                    answers: ["Small", "Medium"],
                    next: [
                        { text: "Correct!", answers: [], next: [] },
                        { text: "Incorrect!", answers: [], next: [] }
                    ]
                }
            ]
        },
        "fed-policy": {
            text: "Fed Policy Game: Ready?",
            answers: ["Yes", "No"],
            next: [
                {
                    text: "What happens to interest rates after a fed policy change?",
                    answers: ["Increase", "Decrease"],
                    next: [
                        { text: "Correct!", answers: [], next: [] },
                        { text: "Incorrect!", answers: [], next: [] }
                    ]
                }
            ]
        }
    };

    let currentGame = null;
    let currentNode = null;

    // ---------------- IntersectionObserver for scroll triggers ----------------
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if(entry.isIntersecting) {

                const gameKey = entry.target.dataset.game;
                if(gameKey && games[gameKey]){
                    currentGame = games[gameKey];
                    currentNode = currentGame;
                    updateQuestion();
                }

                // Show floating game
                floating.classList.add("active");

                // If minimized, temporarily restore image + question + close button
                if(floating.classList.contains("minimized")){
                    floatingImage.style.opacity = "1";
                    questionContainer.style.opacity = "1";
                    questionContainer.style.pointerEvents = "auto";
                    closeBtn.style.opacity = "1";
                    closeBtn.style.pointerEvents = "auto";
                } else {
                    // Ensure question and buttons are visible and clickable
                    questionContainer.style.opacity = "1";
                    questionContainer.style.pointerEvents = "auto";
                    closeBtn.style.opacity = "1";
                    closeBtn.style.pointerEvents = "auto";
                }

            } else {
                // Hide when leaving section
                floating.classList.remove("active");

                questionContainer.style.opacity = "0";
                questionContainer.style.pointerEvents = "none";
                closeBtn.style.opacity = "0";
                closeBtn.style.pointerEvents = "none";

                if(!floating.classList.contains("minimized")){
                    floatingImage.style.opacity = "1";
                }
            }
        });
    }, { threshold: 0.5 });

    triggers.forEach(section => observer.observe(section));

    // ---------------- Close button ----------------
    closeBtn.addEventListener("click", () => {
        floating.classList.remove("active");
        questionContainer.style.opacity = "0";
        questionContainer.style.pointerEvents = "none";
        closeBtn.style.opacity = "0";
        closeBtn.style.pointerEvents = "none";

        if(!floating.classList.contains("minimized")){
            floatingImage.style.opacity = "1";
        }
    });

    // ---------------- Minimize button ----------------
    minimizeBtn.addEventListener("click", () => {
        if(floating.classList.contains("minimized")){
            floating.classList.remove("minimized");
            floatingImage.style.opacity = "1";
        } else {
            floating.classList.add("minimized");
            floatingImage.style.opacity = "0";
            questionContainer.style.opacity = "0";
            questionContainer.style.pointerEvents = "none";
            closeBtn.style.opacity = "0";
            closeBtn.style.pointerEvents = "none";
        }
    });

    // ---------------- Update question ----------------
    function updateQuestion() {
        if(!currentNode) return;

        const questionText = document.querySelector('#floating-image-wrapper #question-text');
        const buttons = document.querySelectorAll('#floating-image-wrapper #answers button');

        questionText.innerText = currentNode.text;

        buttons.forEach((btn, i) => {
            if(currentNode.answers[i]) {
                btn.style.display = "block";
                btn.innerText = currentNode.answers[i];
            } else {
                btn.style.display = "none";
            }
        });
    }

    // ---------------- Choose answer ----------------
    window.choose = function(index){
        if(currentNode.next[index]){
            currentNode = currentNode.next[index];
            updateQuestion();
        }
    }

    // Initialize
    updateQuestion();

});
</script>



<section class="content-section trigger-game" data-game="stock-size">
    <h2>Stock Size</h2>
    <p>lol.</p>
</section>

Q: If I give you the choice between a stock of a small, medium or large company, which do you expect to be more risky to invest in, just after a positive fed rate event?

First we must define a metric that allows us to classify the stocks into their sizes! Here we need to aggregate two informations; the price of the stock, as well as the amount of sahres that are bought and sold on a regular basis. Indeed, if we choose to only look at the price of stocks, then a stock of a new, upcoming but still developping small company can be bought by one person at a very large price, say 100$ but no one else does, because it is risky, then the "value" will seem high. On the other hand, if we focus only on volume, then we can mistake a cheap, small company that gets exchange a lot because of rumors and speculation when in fact the company is small. A metric that captures both of the important aspects that make a company valuable, is dollar volume: the product of the price of a stock and the traded volume. It represents the total amount of money that was exchanged for this stock in a day. 

To answer this question, we apply the same strategy as previously; we split the stocks into our three categories: small if the dollar volume is anywhere between 0 and 5 million dollars, medium if it is in the range of 5 to 15 million dollars and large if it is anywhere above. For reference, stocks like Apple, Google or Tesla are well above 1 billion dollars on average.




Then we compare every stock of a given size categroy to all others and count the number of times it has more area above the other stock after a positive fed event when plotting the normalized return over time. This can be with a binomial test, by creating noise in the data to determine how "close" such an experiment is to give a different outcome. We obtian the following result:

<div id="posfed_barplot" style="width:100%; height:500px;"></div>

From this plot, we read two things; the first, is that if you where to stick to this generalized question of: which sotck size reacts the best to positive fed events? Then the best answer would be medium (or large as a close second) sized one. We could have guess this behaviour, since positive fed events mean fewer loans and less development for small companies that cannot rely on reputation or external sponsors or partnerships to maintain their revenues. Indeed we see that proportionally, you are around twice as likely to pick a stock that reacts well compared to the average of its class in the medium (or large) class than in the small one. However, we also see that these percentages are at most 5.7 % for the medium class. This value could reach up to 50% meaning that there are in reality only very few stocks that consistenly outperform their peers. This is afterall not too surprising, since it is the unpredictable nature of stocks that make them so challenging. 

We could ask the same question and perform the same analysis for negative fed rate events, the results would be similar:

<div id="negfed_barplot" style="width:100%; height:500px;"></div>

Here, we observe that the small and large stocks both perform well most often. This is explainable as fed rate decreases encourage innovation and thus strenghtens smaller upcoming firms while also consolidating the experienced ones. These events drive the investors to the extremes of the risky but more affordable stocks or the safer bets that are affordable due to an overall healthy economy. Again we see small values that mean a real, deep, general solution is not to be concluded from this.

Have a look at some example of instances, the stock 'AAN' (AutoNation Inc) beats other stocks of its class (small stocks). 'AAN' happens to be one of the best performer under negative fed events!


<div style="margin:20px 0; padding:16px; border:1px solid #e0e0e0; border-radius:8px; background:#fafafa; text-align:center;">
    <div style="font-weight:700; margin-bottom:10px; color:#333;">Performance comparison – hover to play!</div>
    <img
        id="fed-gif-player"
        src="{{ site.baseurl }}/assets/img/size_examples/other_1.png"
        alt="Fed rate events animation"
        style="max-width:100%; height:auto; border-radius:6px; border:1px solid #ddd; background:#fff;"
    />
    <div style="margin-top:10px; display:flex; justify-content:center; gap:10px;">
        <button id="fed-prev" style="padding:8px 12px; border:1px solid #ccc; border-radius:4px; background:#fff; cursor:pointer;">◀ Prev</button>
        <button id="fed-reset" style="padding:8px 12px; border:1px solid #ccc; border-radius:4px; background:#fff; cursor:pointer;">⟲ Reset</button>
        <button id="fed-next" style="padding:8px 12px; border:1px solid #ccc; border-radius:4px; background:#fff; cursor:pointer;">Next ▶</button>
    </div>
</div>

<script>
(function() {
    const img = document.getElementById('fed-gif-player');
    if (!img) return;

    const frameCount = 7; // adjust if you have a different number of frames
    const basePath = '{{ site.baseurl }}/assets/img/size_examples/other_';
    const frameDuration = 1000; // ms per frame
    let idx = 1;
    let timer = null;

    const nextFrame = () => {
        idx = idx >= frameCount ? 1 : idx + 1; // after last frame, wrap to first
        img.src = `${basePath}${idx}.png`;
    };

    const start = () => {
        if (timer) return;
        timer = setInterval(nextFrame, frameDuration);
    };

    const stop = () => {
        if (timer) {
            clearInterval(timer);
            timer = null;
        }
    };

    img.addEventListener('mouseenter', start);
    img.addEventListener('mouseleave', stop);

    const updateFrame = () => {
        img.src = `${basePath}${idx}.png`;
    };

    const prevBtn = document.getElementById('fed-prev');
    const nextBtn = document.getElementById('fed-next');
    const resetBtn = document.getElementById('fed-reset');

    if (prevBtn) prevBtn.addEventListener('click', () => {
        stop();
        idx = idx === 1 ? frameCount : idx - 1;
        updateFrame();
    });

    if (nextBtn) nextBtn.addEventListener('click', () => {
        stop();
        idx = idx === frameCount ? 1 : idx + 1;
        updateFrame();
    });

    if (resetBtn) resetBtn.addEventListener('click', () => {
        stop();
        idx = 1;
        updateFrame();
    });
})();
</script>

We see that it consistantly reaches much better normalized returns after the negative fed evetn of the 27th of April 2017 than competitors!


<section class="content-section trigger-game" data-game="fed-policy">
    <h2>Fed Policy</h2>
    <p>Understanding interest rate changes.</p>
</section>

<!--<svg id="treemap" width="200" height="200"></svg>


 <svg id="treemap" style="width:100%; height:600px;"></svg>

  <script src="https://d3js.org/d3.v7.min.js">
        const svg = d3.select("#treemap");
        const width = parseInt(svg.style("width"));
        const height = parseInt(svg.style("height"));
        // Load your JSON
        d3.json("{{ site.baseurl }}/data/nasdaq_top5.json").then(data => {
        
        // Create a root hierarchy and sum values
        const root = d3.hierarchy(data)
            .sum(d => d.value)         // size of each box
            .sort((a, b) => b.value - a.value);

        // Compute treemap layout
        d3.treemap()
            .size([width, height])
            .paddingInner(2)
            (root);

        // Create a group for each leaf node
        const cell = svg.selectAll("g")
            .data(root.leaves())
            .enter()
            .append("g")
            .attr("transform", d => `translate(${d.x0},${d.y0})`);

        // Draw rectangles
        cell.append("rect")
            .attr("width", d => d.x1 - d.x0)
            .attr("height", d => d.y1 - d.y0)

        // Add stock symbols
        cell.append("text")
            .attr("x", 4)
            .attr("y", 14)
            .attr("fill", "white")
            .attr("font-size", "12px")
            .text(d => d.data.name);

        // Optional: tooltip with market cap
        cell.append("title")
            .text(d => `${d.data.name}\nMarket Cap: ${d.value}`);
        });

  </script> -->
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>


<!--{
          "name": "FTAI",
          "value": 170267128393.2014,
          "company": "Fortress Transportation and Infrastructure Investors LLC Common Shares"
        },-->
<script>
fetch("{{ site.baseurl }}/data/nasdaq_top35.json")
  .then(response => response.json())
  .then(data => {
    const labels = [];
    const parents = [];
    const values = [];
    const customdata = [];

    function traverse(node, parent) {
      labels.push(node.name);
      parents.push(parent);
      values.push(node.value || 0);
      customdata.push(node.company || "");

      if (node.children) {
        node.children.forEach(child => traverse(child, node.name));
      }
    }

    traverse(data, "");

    const logos = {
        "AAPL": "https://logo.clearbit.com/apple.com",
        "MSFT": "https://logo.clearbit.com/microsoft.com"
        };

    
    Plotly.newPlot("treemap", [{
      type: "treemap",
      labels: labels,
      parents: parents,
      values: values,
      customdata: customdata,
      textinfo: "label",
      hovertemplate:
        "<b>%{label}, %{customdata}</b><br>" +
        "Value: %{value} $<extra></extra>"
        //"<img src='https://cdn.brandfetch.io/TSLA?c=1idwdMraqBjRGH9xwqh' height='40' /><extra></extra>"
    }], {  
      margin: { t: 30, l: 0, r: 0, b: 0 }
    });

    });
</script> 

<div id="sunburst" style="width:100%; height:700px;"></div>

<!--<script>
fetch("{{ site.baseurl }}/data/nasdaq_etf_stocks.json")
  .then(response => response.json())
  .then(data => {
    const labels = ["ETFs"];
    const parents = [""];
    const values = [0];
    const colorValues = [0]; // Color for root

    // Add sectors
    const sectors = [...new Set(data.map(d => d.Sector))];
    sectors.forEach(sector => {
      labels.push(sector);
      parents.push("ETFs");
      values.push(0);
      // Sum all stocks in this sector for color
      const sectorValue = data
        .filter(d => d.Sector === sector)
        .reduce((sum, d) => sum + d.Value, 0);
      colorValues.push(sectorValue);
    });

    // Add ETFs
    const etfs = [...new Set(data.map(d => d.ETF))];
    etfs.forEach(etf => {
      const sector = data.find(d => d.ETF === etf).Sector;
      labels.push(etf);
      parents.push(sector);
      values.push(0);
      const etfValue = data
        .filter(d => d.ETF === etf)
        .reduce((sum, d) => sum + d.Value, 0);
      colorValues.push(etfValue);
    });

    // Add individual stocks
    data.forEach(d => {
      labels.push(d.stock);
      parents.push(d.ETF);
      values.push(d.Value);
      colorValues.push(d.Value);
    });

    Plotly.newPlot("sunburst", [{
      type: "sunburst",
      labels: labels,
      parents: parents,
      values: values,
      //branchvalues: 'total',
      marker: {
        colors: colorValues,
        colorscale: 'RdBu',
        showscale: true
      },
      hovertemplate: "%{label}<br>Dollar volume: %{value} $<extra></extra>"
    }], {
      margin: { t: 50, l: 0, r: 0, b: 0 }
    });
  });
</script>--> 
<!--
<script>
fetch("{{ site.baseurl }}/data/nasdaq_etf_stocks.json")
  .then(response => response.json())
  .then(data => {
    const labels = ["ETFs"];
    const parents = [""];
    const values = [0]; // Will update later

    // Extract unique sectors
    const sectors = [...new Set(data.map(d => d.Sector))];

    // Compute sector totals
    const sectorTotals = {};
    sectors.forEach(sector => {
      const total = data
        .filter(d => d.Sector === sector)
        .reduce((sum, d) => sum + d.Value, 0);
      sectorTotals[sector] = total;

      labels.push(sector);
      parents.push("ETFs");
      values.push(total);
    });

    // Extract unique ETFs
    const etfs = [...new Set(data.map(d => d.ETF))];

    // Compute ETF totals
    const etfTotals = {};
    etfs.forEach(etf => {
      const total = data
        .filter(d => d.ETF === etf)
        .reduce((sum, d) => sum + d.Value, 0);
      etfTotals[etf] = total;

      const sector = data.find(d => d.ETF === etf).Sector;
      labels.push(etf);
      parents.push(sector);
      values.push(total);
    });

    // Add individual stocks
    data.forEach(d => {
      labels.push(d.stock);
      parents.push(d.ETF);
      values.push(d.Value);
    });

    // Create a color array using a continuous color scale
    const maxVal = Math.max(...values);
    const minVal = Math.min(...values);

    const colors = values.map(v => {
      const t = (v - minVal) / (maxVal - minVal); // normalize to 0-1
      return t; // Plotly will map this to the colorscale
    });

    // Create sunburst with a color gradient
    Plotly.newPlot("sunburst", [{
      type: "sunburst",
      labels: labels,
      parents: parents,
      values: values,
      branchvalues: 'total',
      hovertemplate: "%{label}<br>Dollar volume: %{value} $<extra></extra>",
      marker: {
        colors: colors,
        colorscale: 'Viridis', // choose any built-in color scale
        showscale: true        // shows the color scale legend
      }
    }], {
      margin: { t: 50, l: 0, r: 0, b: 0 }
    });
  });
</script> -->


<script>
fetch("{{ site.baseurl }}/data/nasdaq_etf_stocks.json")
  .then(response => response.json())
  .then(data => {
    const labels = ["ETFs"];
    const parents = [""];
    const values = [0]; // Will update later

    // Extract unique sectors
    const sectors = [...new Set(data.map(d => d.Sector))];

    // Compute sector totals
    const sectorTotals = {};
    sectors.forEach(sector => {
      const total = data
        .filter(d => d.Sector === sector)
        .reduce((sum, d) => sum + d.Value, 0);
      sectorTotals[sector] = total;

      labels.push(sector);
      parents.push("ETFs");
      values.push(total); // <-- parent total = sum of children
    });

    // Extract unique ETFs
    const etfs = [...new Set(data.map(d => d.ETF))];

    // Compute ETF totals
    const etfTotals = {};
    etfs.forEach(etf => {
      const total = data
        .filter(d => d.ETF === etf)
        .reduce((sum, d) => sum + d.Value, 0);
      etfTotals[etf] = total;

      const sector = data.find(d => d.ETF === etf).Sector;
      labels.push(etf);
      parents.push(sector);
      values.push(total); // <-- ETF total
    });

    // Add individual stocks
    data.forEach(d => {
      labels.push(d.stock);
      parents.push(d.ETF);
      values.push(d.Value);
    });

    // Create sunburst
    Plotly.newPlot("sunburst", [{
      type: "sunburst",
      labels: labels,
      parents: parents,
      values: values,
      //branchvalues: 'total', // now safe
      hovertemplate: "%{label}<br>Dollar volume: %{value} $<extra></extra>"
    }], {
      margin: { t: 50, l: 0, r: 0, b: 0 }
    });
  });
</script>


<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>

<script>
fetch("{{ site.baseurl }}/data/posfed_event_size_results.json")
  .then(response => response.json())
  .then(data => {

    const x = data.map(d => d.size);
    const y = data.map(d => d.value);

    const trace = {
      type: "bar",
      x: x,
      y: y,
      marker: {
        color: y,                
        colorscale: "RdBu",
        cmin: 0,                 
        cmax: 8,                
        showscale: true,
        colorbar: {
          title: "Scale",
          tickvals: [0, 2, 4, 6, 8, 10]
        }
      },
      hovertemplate:
        "<b>%{x}</b><br>" +
        "Percentage of dominant stocks: %{y:.2f} %<extra></extra>"
    };

    const layout = {
      title: {
        text: "Percentage of Dominant Stocks After Positive Fed Events",
        x: 0.5
      },
      yaxis: {
        title: "Percentage of dominant stocks (%)"
      },
      xaxis: {
        title: "Size Category"
      },
      margin: { t: 60, l: 60, r: 60, b: 60 }
    };

    Plotly.newPlot("posfed_barplot", [trace], layout, { responsive: true });
  });
</script>


<script>
fetch("{{ site.baseurl }}/data/negfed_event_size_results.json")
  .then(response => response.json())
  .then(data => {

    const x = data.map(d => d.size);
    const y = data.map(d => d.value);

    const trace = {
      type: "bar",
      x: x,
      y: y,
      marker: {
        color: y,                
        colorscale: "RdBu",
        cmin: 0,                 
        cmax: 8,                
        showscale: true,
        colorbar: {
          title: "Scale",
          tickvals: [0, 2, 4, 6, 8, 10]
        }
      },
      hovertemplate:
        "<b>%{x}</b><br>" +
        "Percentage of dominant stocks: %{y:.2f} %<extra></extra>"
    };

    const layout = {
      title: {
        text: "Percentage of Dominant Stocks After Negative Fed Events",
        x: 0.5
      },
      yaxis: {
        title: "Percentage of dominant stocks (%)"
      },
      xaxis: {
        title: "Size Category"
      },
      margin: { t: 60, l: 60, r: 60, b: 60 }
    };

    Plotly.newPlot("negfed_barplot", [trace], layout, { responsive: true });
  });
</script>


<!--Plotly.newPlot("treemap", [{
      type: "treemap",
      labels: labels,
      parents: parents,
      values: values,
      textinfo: "label",
      hovertemplate:
        "<b>%{label}</b><br>" +
        "Value: %{value}<extra></extra>"
    }], {
    
    
    Plotly.newPlot('treemap', [{
        type: "treemap",
        labels: ["Technology","AAPL","MSFT"],
        parents: ["","Technology","Technology"],
        values: [0,2500,2300],
        customdata: ["","https://cdn.brandfetch.io/TSLA?c=1idwdMraqBjRGH9xwqh","https://cdn.brandfetch.io/TSLA?c=1idwdMraqBjRGH9xwqh"],
        hovertemplate: "<b>%{label}</b><br>"+"<img src='%{customdata}' alt='Logo by Brandfetch' /><extra></extra>"
    }]
    {-->
