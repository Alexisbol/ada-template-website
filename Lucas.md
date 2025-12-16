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

One of the questions that we asked ourselves was to study what the impact of fed rates on two comparable companies, given a comparison criterion, can reveal on the specifics of the companies. The idea is to study the reactions and reactivities to fed rates events and link different reactions to different underlying truths about the companies, their functionning and economic strategies.


## Idea behing the Analysis

A relevant analysis of the impact of the fed rates ask for a relevant difference in the behavior of the two companies we are focusing on. The idea behind this work therefore lies in defining a comparability measure and finding pairs of companies both strongly comparable before the event, and significantly different after. We can then sort all pairs given this criterion to focus only on the more intersting cases.

 
## Comparability Methods 

A first comment goes towards the sectors of the companies. To achieve the relevant analysis that we had in mind, we chose to only consider pairs of companies lying within the same sector. This way the results cannot be biased by between-sectors difference in behaviors. We based the rest of our approach of comparability on the features of the companies 

A first obstacle in the definition of a comparabilty measure lies in the volatility of these features along a time period.
The solution adopted was therefore to think of a local measure of how similar two companies are on a given small time period. This approach fit our case as we aim to study the impact of localized fed rate events, hence the evolution of the before and after the event for two companies. The idea is then to define a small time window on which we can compare the values of a given feature for both companies.

The issue that arises with this method, and second obstacle, is to account for outliers, meaning localized behaviors of the features that are not inscribed in the global trend of the window. As the idea is to ultimaetely define a similarity metric, that is a number, the idea that we had to nullify the impact of these outliers in theory is to consider the median of the values that the feature takes. Like we said, This approach has the adventage to limit the influence of the outliers when summarizing the behavior of the feature, in opposition to a mean that would be highly reactive to the former.

A Third obstacle lied in the fact that we were that so far we were comparing raw values, without considering the scales of the features. In fact, when dealing with objects that come in a vast diversity like companies, it is important to account for their scale, because what can be a huge change in raw numbers can turn out to be a minor event in the eye of an even bigger company. In that sense, a raw numbers approach would discard any pairs of large scale companies during the sorting. The solution that we adopted was to consider the Bray-Curtis dissimalirity which brings back a difference in raw numbers to the scale of these numbers themselves. 

Once all these obstacles had been tackled we ended up with the complete method for comparing two companies, which can be summarized in the following equation 

> 
>  <img src="assets/img/Lucas/comparability_measure.png" height="70em">
>
> With X̃ the median of the feature considered for the company X during the time window considered 
>


## Focus on the Features

Given the comparaison method that we had derive, we had to find which feature of a company would best express this notion of comparibility we had in mind. Having already taken care of the sector of the company, the idea of comparability lied intuitively in a notion of "size" of the company. We have already discussed this notion in the part on the size dependent analysis, but as a reminder the idea is here to compare companies of "similar" "size". We have defined this concept of "similar" already what is left is to look into how different features, both given by the dataset and engineered ourseleves could better represent the "size" of a company.

We first considered features like Volume of shares exchanged and Return. Now the latter is already an engineered feature, defined as the percentage of difference between two Closing prices distanced by a given time period (generally for us 21 days). The issue that arised from these features was their lack of complete economical grounding. In fact we can imagine a company that has issued a large amount of consequently cheap shares, which would imply that a large quantity of exchanged shares doesn't necesseraily represent a large amount of money exchanged. Similarly, a big difference in Closing prices in a compay with a low amount of shares issued doesn't necessarily represent an important financial gain or loss. The reader may have realized that one lacks the other offers, the idea is then to combine the notions behind them into composite features that display a more complete economical grounding.

The feature created from this conclusion is called Dollar Volume and depends on a third one called Typical price. The latter is a well known feature used in finance and that is defined as a weighted average of all the prices of a share (Opening, Closing, Highest, Lowest). This feature helps us define a more adaptable and all encompassing notion of price for a company share. We then define our Dollar Volume as the product of the amount of shares traded and the typical price of a share, to get a quantifier of the amount of financial volume traded.

On a side note, we also defined a feature called Dollar Return as the product between the Return and the Typical price that helps us in the analysis to better quantify the gains or losses of a company in monitary terms.


## Relevance of the Results

One key ingredient is missing to the pipeline so far. Everything mentioned combined only offers an automized way to get pairs of companies with the most intersting properties of similarity for our analysis, but it never guarantees the existence of the statistical significance of said properties. What we mean is the fact that we merely sort the pairs based on a similarity and dissimilarity score to get companies the most similar at the beginning and most different at the end of the event, but nothing in the process guarantees that these difference are statistically significative. 

The solution found was to introduce different t-test at different steps of the pipeline to study their p values. In that sense we have t-test for the evolution of the feature of the company, in order to quantify a real impact on these features. In addition we have t-test comparing both companies on the start and end windows of the event to test the significance of the start similarity and end dissimilarity mentionned previously.

These tests allow us to only discuss significant changes in the behavior of the companies, but not to assess the role of the fed rates in those changes. A last step towards the relevance of our results was then to introduce correlations and linear regressions to study the link between these evolutions in the features of the company and the evolution of the fed rate.


## Case studies

Through the different aspect of this research question we have defined a fully functionning pipeline aiming to produce pairs of companies judged "comparable" along with the significance of this judgement. Nevertheless, the real analysis lies past this pipeline and focuses rather on its product. We thus select the most relevant cases to pursue and analyse what different behaviors from comparable companies can reveal about their functionning. 


<style>
  .image-configurator {
    position: relative;
    width: 700px;
    max-width: 100%;
    aspect-ratio: 3 / 2;
    border: 1px solid #ccc;
    font-family: Arial, sans-serif;
    overflow: hidden;
  }

  .image-configurator img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    background: #fafafa;
  }

  .menu {
    position: absolute;
    top: 10px;
    min-width: 160px;
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid #aaa;
    z-index: 10;
  }

  .menu.left { left: 10px; }
  .menu.right { right: 10px; }

  .menu-header {
    padding: 6px 8px;
    cursor: pointer;
    background: #f4f4f4;
    user-select: none;
    font-weight: bold;
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
  }

  .menu-content div {
    padding: 6px 8px;
    cursor: pointer;
  }

  .menu-content div:hover {
    background: #d0d0d0;
  }

  .menu.open .menu-content {
    display: block;
  }
</style>

<div class="image-configurator">
  <img id="mainImage" alt="Selected image">

  <div class="menu left" id="categoryMenu">
    <div class="menu-header">Category</div>
    <div class="menu-content"></div>
  </div>

  <div class="menu right" id="imageMenu">
    <div class="menu-header">Image</div>
    <div class="menu-content"></div>
  </div>
</div>

<script>
  // YOUR IMAGES — UNCHANGED PATHS
  const images = {
    Companies: [
      { label: "pair1", src: "{{ site.baseurl }}/assets/img/recruiter.png" },
      { label: "pair2", src: "{{ site.baseurl }}/assets/images/recruiter.png" }
    ],
    Feature: [
      { label: "feature1", src: "{{ site.baseurl }}/assets/img/X_tilde.png" },
      { label: "feature2", src: "{{ site.baseurl }}/assets/img/comparability_mesure.png" }
    ]
  };

  const mainImage = document.getElementById("mainImage");

  const categoryMenu = document.getElementById("categoryMenu");
  const imageMenu = document.getElementById("imageMenu");

  const categoryContent = categoryMenu.querySelector(".menu-content");
  const imageContent = imageMenu.querySelector(".menu-content");

  let currentCategory = Object.keys(images)[0];

  function closeMenus() {
    categoryMenu.classList.remove("open");
    imageMenu.classList.remove("open");
  }

  function loadCategories() {
    categoryContent.innerHTML = "";
    Object.keys(images).forEach(cat => {
      const item = document.createElement("div");
      item.textContent = cat;
      item.onclick = () => {
        currentCategory = cat;
        categoryMenu.querySelector(".menu-header").textContent = cat;
        loadImages(cat);
        closeMenus();
      };
      categoryContent.appendChild(item);
    });
  }

  function loadImages(category) {
    imageContent.innerHTML = "";
    images[category].forEach(img => {
      const item = document.createElement("div");
      item.textContent = img.label;
      item.onclick = () => {
        mainImage.src = img.src;
        imageMenu.querySelector(".menu-header").textContent = img.label;
        closeMenus();
      };
      imageContent.appendChild(item);
    });
  }

  // Toggle menus
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

  // Init
  loadCategories();
  loadImages(currentCategory);
  mainImage.src = images[currentCategory][0].src;
  categoryMenu.querySelector(".menu-header").textContent = currentCategory;
  imageMenu.querySelector(".menu-header").textContent = images[currentCategory][0].label;
</script>



### _Accuracy Inc_ VS _Davita Inc_

The first intersting case is that of these two companies, from the Healthcare sector.


### _Art’s Way manufacturing Co Inc_ VS _Argan Inc_

The first intersting case is that of these two companies, from the Industry sector.


### _Astrotech Corp_ VS _AstraNova Inc_

The first intersting case is that of these two companies, from the Technology sector.


### _Devon Energy Corp_ VS _Murphy Oil Corp_

The first intersting case is that of these two companies, from the Energy sector.
