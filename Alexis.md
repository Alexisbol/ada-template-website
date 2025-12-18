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

# def fed events (+ parameters in our dataset) (Alexis)
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

# ETF / stock (method & results & graphs & interpretation / intuition)

1. Identify for rate signals (see previous explanation)
2. Map etf and corresponding stocks. Each ETF countains multiple stocks, for example for an ETF about the Technological sector, the ETF "XLK" includes stocks like "AAPL", "MSFT", etc.
We only pair the important stocks of an ETF with the stock itself.
3. for each etf and one of the corresponding stocks, we compute the performance during each fed rate event.
4. If the etf or the stocks performs better a significant amount of time computed with a binomtest. Than we store the result.

5. Finally we can display the results in a table.


<img src="{{ site.baseurl }}/assets/img/etfvsstocksevent_sign.png" alt="Fed Rate Event Results Table" style="max-width:100%; height:auto; border-radius:6px; border:1px solid #ddd; background:#fff;"/>

<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>

<div style="margin:30px 0;padding:24px;border:1px solid #e1e8f0;border-radius:14px;background:#fbfdff;box-shadow:0 10px 24px rgba(12,50,96,0.08);">
    <h3 style="margin:0 0 12px;color:#0d1b2a;">📊 Interactive: ETF vs Stock Performance by Event Type</h3>
    <p style="margin:0 0 16px;color:#2f3f55;">
        Compare how ETFs and individual stocks perform during positive (rate increases) vs negative (rate cuts) Fed events. 
        Hover over the bars to see exact counts.
    </p>
    <div id="overallWinsInteractive" style="width:100%;height:450px;"></div>
</div>

<script>
(function() {
    async function loadAndPlotOverallWins() {
        try {
            const response = await fetch('{{ site.baseurl }}/data/all_fed_outperformance.json');
            const text = await response.text();
            const lines = text.trim().split('\n');
            const data = lines.map(line => JSON.parse(line));
            
            // Count winners by type and Fed sign
            const counts = {
                'ETF (PosFed)': 0,
                'Stock (PosFed)': 0,
                'ETF (NegFed)': 0,
                'Stock (NegFed)': 0
            };
            
            data.forEach(d => {
                const key = `${d.Winner} (${d.Fed_sign_type})`;
                counts[key] = (counts[key] || 0) + 1;
            });
            
            const trace1 = {
                x: ['Positive Fed Events<br>(Rate Increases)', 'Negative Fed Events<br>(Rate Cuts)'],
                y: [counts['ETF (PosFed)'], counts['ETF (NegFed)']],
                name: 'ETF Wins',
                type: 'bar',
                marker: { 
                    color: '#0ea5e9',
                    line: { color: '#0284c7', width: 1.5 }
                },
                text: [counts['ETF (PosFed)'], counts['ETF (NegFed)']],
                textposition: 'outside',
                textfont: { size: 14, color: '#0ea5e9', weight: 'bold' },
                hovertemplate: '<b>ETF Wins</b><br>Count: %{y}<br><extra></extra>'
            };
            
            const trace2 = {
                x: ['Positive Fed Events<br>(Rate Increases)', 'Negative Fed Events<br>(Rate Cuts)'],
                y: [counts['Stock (PosFed)'], counts['Stock (NegFed)']],
                name: 'Stock Wins',
                type: 'bar',
                marker: { 
                    color: '#8b5cf6',
                    line: { color: '#7c3aed', width: 1.5 }
                },
                text: [counts['Stock (PosFed)'], counts['Stock (NegFed)']],
                textposition: 'outside',
                textfont: { size: 14, color: '#8b5cf6', weight: 'bold' },
                hovertemplate: '<b>Stock Wins</b><br>Count: %{y}<br><extra></extra>'
            };
            
            const layout = {
                barmode: 'group',
                plot_bgcolor: '#f8fafc',
                paper_bgcolor: 'transparent',
                font: { family: 'Noto Sans, sans-serif', size: 13 },
                xaxis: { 
                    title: '',
                    gridcolor: '#e2e8f0',
                    tickfont: { size: 12, weight: 'bold' }
                },
                yaxis: { 
                    title: 'Number of Significant Pairs',
                    gridcolor: '#e2e8f0',
                    tickfont: { size: 11 },
                    titlefont: { size: 13, weight: 'bold' }
                },
                legend: { 
                    orientation: 'h',
                    x: 0.5,
                    xanchor: 'center',
                    y: 1.12,
                    bgcolor: 'rgba(255,255,255,0.9)',
                    bordercolor: '#e2e8f0',
                    borderwidth: 1,
                    font: { size: 12 }
                },
                margin: { t: 80, r: 40, b: 80, l: 70 },
                hoverlabel: {
                    bgcolor: 'white',
                    bordercolor: '#e2e8f0',
                    font: { size: 12, family: 'Noto Sans, sans-serif' }
                }
            };
            
            const config = {
                responsive: true,
                displayModeBar: true,
                displaylogo: false,
                modeBarButtonsToRemove: ['lasso2d', 'select2d']
            };
            
            Plotly.newPlot('overallWinsInteractive', [trace1, trace2], layout, config);
            
        } catch (error) {
            console.error('Error loading overall wins data:', error);
        }
    }
    
    if (typeof Plotly !== 'undefined') {
        loadAndPlotOverallWins();
    } else {
        window.addEventListener('load', loadAndPlotOverallWins);
    }
})();
</script>

We can see that when there is a positive fed event (FED rate increase), Stocks tend to react better than ETF. 
On the contrary, when there is a negative FED event (FED rate decrease), ETF tend to react better.

### Now let's look at inside specific sectors

<img src="{{ site.baseurl }}/assets/img/etfvsstocksevent_negfed_sector.png" alt="Fed Rate Event Results Table" style="max-width:100%; height:auto; border-radius:6px; border:1px solid #ddd; background:#fff;"/>

<img src="{{ site.baseurl }}/assets/img/etfvsstocksevent_posfed_sector.png" alt="Fed Rate Event Results Table" style="max-width:100%; height:auto; border-radius:6px; border:1px solid #ddd; background:#fff;"/>


If we look closer on the positive fed event, we can see that Stocks, is clearly wining in Healthcare and industrial sectors, winning in technology, losing in consumer cyclical and clearly losing in financial services.

Now, let’s focus on the Negative fed event. We can see the same trend for Consumer Cyclical Financial Services, Healthcare.

However, for Industrial, ETF are winning, same in technology.

# TODO ADD eplanation...

# ADD last interactive cool plot to see companies reacting well to positive or/and negative FED events.
## This but interactive

<img src="{{ site.baseurl }}/assets/img/comparaison_fed_event_companies.png" alt="Fed Rate Event Results Table" style="max-width:100%; height:auto; border-radius:6px; border:1px solid #ddd; background:#fff;"/>

---

## Interactive Analysis: ETF vs Stock Performance

<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>

<div style="margin:30px 0;padding:24px;border:1px solid #e1e8f0;border-radius:14px;background:#fbfdff;box-shadow:0 10px 24px rgba(12,50,96,0.08);">
    <h3 style="margin:0 0 12px;color:#0d1b2a;">📊 Overall Winner Distribution</h3>
    <p style="margin:0 0 16px;color:#2f3f55;">
        Distribution of winners across all Fed rate events, comparing ETF vs Stock performance.
    </p>
    <div id="overallWinsChart" style="width:100%;height:500px;"></div>
</div>

<div style="margin:30px 0;padding:24px;border:1px solid #e1e8f0;border-radius:14px;background:#fbfdff;box-shadow:0 10px 24px rgba(12,50,96,0.08);">
    <h3 style="margin:0 0 12px;color:#0d1b2a;">📈 Positive Fed Events: Winners by Sector</h3>
    <p style="margin:0 0 16px;color:#2f3f55;">
        When the Fed <strong>increases rates</strong> (tightening policy), how do ETFs vs Stocks perform across different sectors?
    </p>
    <div id="posFedSectorChart" style="width:100%;height:550px;"></div>
</div>

<div style="margin:30px 0;padding:24px;border:1px solid #e1e8f0;border-radius:14px;background:#fbfdff;box-shadow:0 10px 24px rgba(12,50,96,0.08);">
    <h3 style="margin:0 0 12px;color:#0d1b2a;">📉 Negative Fed Events: Winners by Sector</h3>
    <p style="margin:0 0 16px;color:#2f3f55;">
        When the Fed <strong>decreases rates</strong> (loosening policy), how do ETFs vs Stocks perform across different sectors?
    </p>
    <div id="negFedSectorChart" style="width:100%;height:550px;"></div>
</div>

<script>
(function() {
    // Load all three JSON files
    async function loadAllData() {
        try {
            const [allRes, posRes, negRes] = await Promise.all([
                fetch('{{ site.baseurl }}/data/all_fed_outperformance.json'),
                fetch('{{ site.baseurl }}/data/positive_fed_outperformance.json'),
                fetch('{{ site.baseurl }}/data/negative_fed_outperformance.json')
            ]);
            
            const [allText, posText, negText] = await Promise.all([
                allRes.text(),
                posRes.text(),
                negRes.text()
            ]);
            
            const allData = allText.trim().split('\n').map(line => JSON.parse(line));
            const posData = posText.trim().split('\n').map(line => JSON.parse(line));
            const negData = negText.trim().split('\n').map(line => JSON.parse(line));
            
            return { allData, posData, negData };
        } catch (error) {
            console.error('Error loading data:', error);
            return { allData: [], posData: [], negData: [] };
        }
    }
    
    // Plot 1: Overall Winner Distribution (using all_fed_outperformance.json)
    function plotOverallWins(allData) {
        // Count winners by type and Fed sign
        const counts = {
            'ETF (PosFed)': 0,
            'Stock (PosFed)': 0,
            'ETF (NegFed)': 0,
            'Stock (NegFed)': 0
        };
        
        allData.forEach(d => {
            const key = `${d.Winner} (${d.Fed_sign_type})`;
            counts[key] = (counts[key] || 0) + 1;
        });
        
        const trace1 = {
            x: ['Positive Fed Events', 'Negative Fed Events'],
            y: [counts['ETF (PosFed)'], counts['ETF (NegFed)']],
            name: 'ETF Wins',
            type: 'bar',
            marker: { color: '#0ea5e9' },
            text: [counts['ETF (PosFed)'], counts['ETF (NegFed)']],
            textposition: 'auto',
        };
        
        const trace2 = {
            x: ['Positive Fed Events', 'Negative Fed Events'],
            y: [counts['Stock (PosFed)'], counts['Stock (NegFed)']],
            name: 'Stock Wins',
            type: 'bar',
            marker: { color: '#8b5cf6' },
            text: [counts['Stock (PosFed)'], counts['Stock (NegFed)']],
            textposition: 'auto',
        };
        
        const layout = {
            barmode: 'group',
            plot_bgcolor: '#f8fafc',
            paper_bgcolor: 'transparent',
            font: { family: 'Noto Sans, sans-serif', size: 13 },
            xaxis: { title: '', gridcolor: '#e2e8f0' },
            yaxis: { title: 'Number of Wins', gridcolor: '#e2e8f0' },
            legend: { 
                orientation: 'h',
                x: 0.5,
                xanchor: 'center',
                y: -0.15
            },
            margin: { t: 20, r: 20, b: 60, l: 60 }
        };
        
        const config = {
            responsive: true,
            displayModeBar: false
        };
        
        Plotly.newPlot('overallWinsChart', [trace1, trace2], layout, config);
    }
    
    // Plot 2 & 3: Winners by Sector (using specific positive/negative JSON files)
    function plotWinsBySector(data, divId, title) {
        // Group by sector and winner
        const sectorData = {};
        data.forEach(d => {
            if (!sectorData[d.Sector]) {
                sectorData[d.Sector] = { ETF: 0, Stock: 0 };
            }
            sectorData[d.Sector][d.Winner]++;
        });
        
        const sectors = Object.keys(sectorData).sort();
        const etfWins = sectors.map(s => sectorData[s].ETF || 0);
        const stockWins = sectors.map(s => sectorData[s].Stock || 0);
        
        const trace1 = {
            x: sectors,
            y: etfWins,
            name: 'ETF Wins',
            type: 'bar',
            marker: { color: '#0ea5e9' },
            text: etfWins,
            textposition: 'auto',
            hovertemplate: '<b>%{x}</b><br>ETF Wins: %{y}<extra></extra>'
        };
        
        const trace2 = {
            x: sectors,
            y: stockWins,
            name: 'Stock Wins',
            type: 'bar',
            marker: { color: '#8b5cf6' },
            text: stockWins,
            textposition: 'auto',
            hovertemplate: '<b>%{x}</b><br>Stock Wins: %{y}<extra></extra>'
        };
        
        const layout = {
            barmode: 'group',
            plot_bgcolor: '#f8fafc',
            paper_bgcolor: 'transparent',
            font: { family: 'Noto Sans, sans-serif', size: 12 },
            xaxis: { 
                title: '',
                tickangle: -35,
                gridcolor: '#e2e8f0'
            },
            yaxis: { 
                title: 'Number of Wins',
                gridcolor: '#e2e8f0'
            },
            legend: { 
                orientation: 'h',
                x: 0.5,
                xanchor: 'center',
                y: -0.25
            },
            margin: { t: 20, r: 20, b: 100, l: 60 }
        };
        
        const config = {
            responsive: true,
            displayModeBar: false
        };
        
        Plotly.newPlot(divId, [trace1, trace2], layout, config);
    }
    
    // Initialize all plots
    async function init() {
        const { allData, posData, negData } = await loadAllData();
        if (allData.length === 0) return;
        
        plotOverallWins(allData);
        plotWinsBySector(posData, 'posFedSectorChart', 'Positive Fed Events');
        plotWinsBySector(negData, 'negFedSectorChart', 'Negative Fed Events');
    }
    
    // Load when ready
    if (typeof Plotly !== 'undefined') {
        init();
    } else {
        window.addEventListener('load', init);
    }
})();
</script>

### Key Insights

**Overall Patterns:**
- During **positive Fed events** (rate increases), individual stocks tend to outperform their sector ETFs, particularly in Healthcare and Industrial sectors
- During **negative Fed events** (rate cuts), ETFs show stronger resilience, especially in Technology and Financial sectors

**Sector-Specific Behaviors:**
- **Technology**: Stocks dominate during rate hikes, but ETFs provide better stability during cuts
- **Healthcare**: Stocks consistently outperform across both event types, showing sector-specific strength
- **Financials**: ETFs win decisively during rate cuts, benefiting from diversification during volatile periods
- **Energy**: Mixed results with sector volatility playing a major role

This analysis reveals that diversification (ETFs) becomes more valuable during Fed easing cycles, while concentrated bets (individual stocks) can outperform during tightening cycles in specific sectors.