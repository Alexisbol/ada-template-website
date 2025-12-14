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
        <a href="{{ site.baseurl }}/game" class="nav-link">Interactive</a>
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


We based our approach of comparability on the features of the dataset, and composite features based on the former.

__maybe put here graphs of the composite__


A first obstacle in the definition of a comparabilty measure lies in the volatility of these features along a time period.
The solution adopted was therefore to think of a local measure of how similar two companies are on a given small time period. This approach fit our case as we aim to study the impact of localized fed rate events, hence the evolution of the before and after the event for two companies. The idea is then to define a small time window on which we can compare the values of a given feature for both companies.

The issue that arises with this method, and second obstacle, is to account for outliers, meaning localized behaviors of the features that are not inscribed in the global trend of the window. As the idea is to ultimaetely define a similarity metric, that is a number, the idea that we had to nullify the impact of these outliers in theory is to consider the median of the values that the feature takes. Like we said, This approach has the adventage to limit the influence of the outliers when summarizing the behavior of the feature, in opposition to a mean that would be highly reactive to the former.

A Third obstacle lied in the fact that we were that so far we were comparing raw values, without considering the scales of the features. In fact, when dealing with objects that come in a vast diversity like companies, it is important to account for their scale, because what can be a huge change in raw numbers can turn out to be a minor event in the eye of an even bigger company. In that sense, a raw numbers approach would discard any pairs of large scale companies during the sorting. The solution that we adopted was to consider the Bray-Curtis dissimalirity which brings back a difference in raw numbers to the scale of these numbers themselves. 

Once all these obstacles had been tackled we ended up with the complete method for comparing two companies, which can be summarized in the following equation 

> 
>  <img src="assets/img/Lucas/comparability_measure.png" height="30em">
>
> With X̃ the median of the feature considered for the company X during the time window considered 
>



## Case studies