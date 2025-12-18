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
        <a href="{{ site.baseurl }}/Lucas" class="nav-link">Lucas</a>
        <a href="{{ site.baseurl }}/Alexis" class="nav-link active">Alexis</a>
        <a href="{{ site.github.repository_url }}" class="nav-link" target="_blank">Repository</a>
    </div>
</div>

## def fed events (+ parameters in our dataset) (Alexis)
We want to focus our analysis on specific Federal Reserve interest rate events.
Specifically, we aim to detect periods in which the Fed rate experiences a **substantial increase or decrease**, followed by a **stable phase lasting a few days**.  
This allows us to study market behavior during intervals when the interest rate remains constant — ensuring that our observations are not influenced by additional policy changes occurring in the same timeframe.

<span style="color:#d40000; font-weight:700;">Positive Fed Event (red)</span>: tightening to slow the economy or curb inflation, then stepping back to let the market absorb the change.

<span style="color:#008800; font-weight:700;">Negative Fed Event (green)</span>: loosening to stimulate growth or combat a recession.


<details>
<summary><strong>Algorithm</strong></summary>

<p>We created an algorithm to identify such events in our dataset. The <code>identify_fed_rate_signals</code> function detects significant Federal Reserve rate changes with the following parameters:</p>

<ul>
<li><strong>window_size</strong> (28 days): Number of days in the sliding window for baseline calculation</li>
<li><strong>transition_window</strong> (3 days): Number of days to search ahead for the maximum delta. The day with the largest absolute change will be selected as signal start</li>
<li><strong>central_metric</strong> ("robust"): Statistical metric to use as the center of the sliding window baseline. Options: 'mean', 'median', or 'robust' (average of mean and median)</li>
<li><strong>alfa</strong> (0.8): Fraction of standard deviation to define uncertainty range around both the baseline and the delta</li>
<li><strong>min_delta</strong> (0.2%): Minimum absolute change in Fed rate to qualify as a signal. The entire uncertainty range must be above this threshold</li>
<li><strong>max_delta</strong> (2%): Maximum absolute change in Fed rate to qualify as a signal. The entire uncertainty range must be below this threshold</li>
<li><strong>skip_days</strong> (5 days): Number of days to skip after identifying a signal to avoid detecting consecutive related signals</li>
<li><strong>stability_days</strong> (21 days): Number of days following a signal to check for stability</li>
<li><strong>stability_fraction</strong> (0.5): Fraction of delta to define the acceptable stability range. E.g., 0.5 means Fed rate can vary by ±50% of the initial change</li>
</ul>

</details>


<div style="margin:20px 0; padding:16px; border:1px solid #e0e0e0; border-radius:8px; background:#fafafa; text-align:center;">
    <div style="font-weight:700; margin-bottom:10px; color:#333;">Fed rate events – hover to play!</div>
    <img
        id="fed-gif-player"
        src="{{ site.baseurl }}/assets/img/fed_rate_event/fed_rate_event_1.png"
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

    const frameCount = 10; // adjust if you have a different number of frames
    const basePath = '{{ site.baseurl }}/assets/img/fed_rate_event/fed_rate_event_';
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

### Now we can take a look at all the identified Fed rate events in our dataset

<iframe src="{{ site.baseurl }}/assets/html/fed_signals_interactive.html" width="100%" height="650" frameborder="0"></iframe>

We can indeed see that the algorithm has indentified recession, for example in 2001, 2008 or 2019 where we see a lot of green (negative Fed events) as the Fed was trying to stimulate the economy.

## ETF / stock (method & results & graphs & interpretation / intuition)

1. Identify for rate signals (see previous explanation)
2. Map etf and corresponding stocks. Each ETF countains multiple stocks, for example for an ETF about the Technological sector, the ETF "XLK" includes stocks like "AAPL", "MSFT", etc.
We only pair the important stocks of an ETF with the stock itself.
3. for each etf and one of the corresponding stocks, we compute the performance during each fed rate event.
4. If the etf or the stocks performs better a significant amount of time computed with a binomtest. Than we store the result.

5. Finally we can display the results in a table.


<img src="{{ site.baseurl }}/assets/img/etfvsstocksevent_sign.png" alt="Fed Rate Event Results Table" style="max-width:100%; height:auto; border-radius:6px; border:1px solid #ddd; background:#fff;"/>

We can see that when there is a positive fed event (FED rate increase), Stocks tend to react better than ETF. 
On the contrary, when there is a negative FED event (FED rate decrease), ETF tend to react better.

### Now let's look at inside specific sectors

<img src="{{ site.baseurl }}/assets/img/etfvsstocksevent_negfed_sector.png" alt="Fed Rate Event Results Table" style="max-width:100%; height:auto; border-radius:6px; border:1px solid #ddd; background:#fff;"/>

<img src="{{ site.baseurl }}/assets/img/etfvsstocksevent_posfed_sector.png" alt="Fed Rate Event Results Table" style="max-width:100%; height:auto; border-radius:6px; border:1px solid #ddd; background:#fff;"/>


If we look closer on the positive fed event, we can see that Stocks, is clearly wining in Healthcare and industrial sectors, winning in technology, losing in consumer cyclical and clearly losing in financial services.

Now, let’s focus on the Negative fed event. We can see the same trend for Consumer Cyclical Financial Services, Healthcare.

However, for Industrial, ETF are winning, same in technology.

## TODO ADD eplanation...

## ADD last interactive cool plot to see companies reacting well to positive or/and negative FED events.
## This but interactive

<img src="{{ site.baseurl }}/assets/img/comparaison_fed_event_companies.png" alt="Fed Rate Event Results Table" style="max-width:100%; height:auto; border-radius:6px; border:1px solid #ddd; background:#fff;"/>