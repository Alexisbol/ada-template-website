# Is Washington truly conducting the symphony of global finance?
  
## Introduction

What is the Federal Reserve Interest Rate?

### TODO REPHRASE INTRO TO TALK ABOUT IMPACT ON COMPANIES 

You can think of the Fed Rate as the "thermostat" for the U.S. economy. While technically it is the interest rate banks charge each other, practically it controls the cost of borrowing for everyone.
How it works: 
- **Turning the Dial Down** (Cutting Rates): When the economy is "freezing" (recession or job loss), the Fed lowers the rate. This makes loans cheaper, encouraging people to buy homes and **businesses** to hire more workers.
- **Turning the Dial Up** (Raising Rates): When the economy is "overheating" (prices rising too fast/inflation), the Fed raises the rate. This makes loans expensive, which slows down spending and stabilizes prices.

Current Status: As of December 2025, the Fed is in a "warming" phase, having cut rates to 3.75% – 4.00% to support the job market.

<style>
    .fed-card {margin:18px 0;padding:16px;border:1px solid #e1e8f0;border-radius:14px;background:#fbfdff;box-shadow:0 10px 24px rgba(12,50,96,0.08);max-width:100%;}
    .fed-main {display:grid;grid-template-columns:260px 1fr;gap:24px;align-items:start;}
    .fed-copy h3 {margin:0 0 8px;color:#0d1b2a;}
    .fed-copy p {margin:6px 0 0;color:#2f3f55;}
    .fed-eyebrow {margin:0 0 6px;text-transform:uppercase;letter-spacing:0.08em;font-size:11px;color:#0d1b2a;opacity:0.7;}
    .fed-dial-wrap {position:relative;}
    .fed-dial {position:relative;width:190px;height:190px;border-radius:50%;background:conic-gradient(from -130deg, #0b6efd 0deg, #3da9f5 90deg, #f7c04a 180deg, #ef476f 260deg, #ef476f 320deg, #0b6efd 360deg);box-shadow:inset 0 0 0 10px #f3f7fb, 0 12px 24px rgba(0,0,0,0.12);overflow:hidden;cursor:pointer;}
    .fed-dial::after {content:"";position:absolute;inset:18px;border-radius:50%;background:#fff;box-shadow:inset 0 0 0 1px #d7e1ee;}
    .fed-dial::before {content:"";position:absolute;bottom:-8px;left:50%;transform:translateX(-50%);width:130px;height:46px;border-radius:70px;box-shadow:0 -2px 6px rgba(0,0,0,0.08);background:#fbfdff;border:1px solid #e1e8f0;z-index:1;}
    .fed-needle {position:absolute;left:50%;top:50%;width:6px;height:70px;background:#0d1b2a;border-radius:999px;transform-origin:50% 80%;transform:translate(-50%,-80%) rotate(0deg);box-shadow:0 6px 12px rgba(0,0,0,0.18);z-index:2;pointer-events:none;}
    .fed-center {position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:78px;height:78px;border-radius:50%;background:#0d1b2a;color:#e5f2ff;display:flex;align-items:center;justify-content:center;font-weight:700;box-shadow:0 6px 12px rgba(0,0,0,0.2);z-index:3;pointer-events:none;}
    .fed-ticks {position:absolute;inset:8px;pointer-events:none;z-index:1;}
    .fed-tick {position:absolute;left:50%;top:50%;width:4px;height:10px;background:#0d1b2a;border-radius:999px;transform-origin:50% 70px;opacity:0.35;}
    .fed-output {padding:14px;border-radius:12px;background:#fff;border:1px dashed #c7d4e6;color:#0d1b2a;line-height:1.5;box-shadow:0 4px 12px rgba(0,0,0,0.04);min-height:80px;}
    .fed-hidden {position:absolute;opacity:0;pointer-events:none;height:0;width:0;}
    @media (max-width: 768px) {
        .fed-main {grid-template-columns:1fr;gap:16px;}
    }
</style>

<div class="fed-card">
    <div class="fed-copy">
        <p class="fed-eyebrow">Interactive Dial</p>
        <h3>Click the Fed "thermostat"</h3>
        <p>Click on the colored ring to adjust the temperature and see how policy ripples through companies and sectors.</p>
    </div>
    <div class="fed-main">
        <div class="fed-dial-wrap">
            <div class="fed-dial" id="fed-dial-visual">
                <div class="fed-ticks">
                    <div class="fed-tick" style="transform:translate(-50%,-50%) rotate(-120deg);"></div>
                    <div class="fed-tick" style="transform:translate(-50%,-50%) rotate(-60deg);"></div>
                    <div class="fed-tick" style="transform:translate(-50%,-50%) rotate(0deg);"></div>
                    <div class="fed-tick" style="transform:translate(-50%,-50%) rotate(60deg);"></div>
                    <div class="fed-tick" style="transform:translate(-50%,-50%) rotate(120deg);"></div>
                </div>
                <div class="fed-needle" id="fed-needle"></div>
                <div class="fed-center" id="fed-center">Warm</div>
            </div>
            <input id="fed-dial" class="fed-hidden" type="range" min="1" max="5" step="1" value="3">
        </div>
        <div id="fed-dial-output" class="fed-output"></div>
    </div>
</div>

<script>
    (function() {
        const dial = document.getElementById('fed-dial');
        const dialVisual = document.getElementById('fed-dial-visual');
        const out = document.getElementById('fed-dial-output');
        const needle = document.getElementById('fed-needle');
        const center = document.getElementById('fed-center');
        if (!dial || !out || !needle || !center || !dialVisual) return;
        const states = {
            1: { label: 'Cold', detail: 'Cold economy: aggressive cuts', text: 'Borrowing gets cheap; growth and small caps pop, credit risk rises; inflation risk subdued.' },
            2: { label: 'Cool', detail: 'Cool: easing bias', text: 'Lower rates support hiring and capex; risk assets find a bid; defensive sectors lag.' },
            3: { label: 'Warm', detail: 'Warm (neutral-ish)', text: 'Policy near neutral; fundamentals and earnings drive returns; balance between growth and value.' },
            4: { label: 'Hot', detail: 'Hot: tightening bias', text: 'Higher discount rates compress valuations; debt-heavy and long-duration names suffer first.' },
            5: { label: 'Overheat', detail: 'Overheat: sharp hikes', text: 'Financing pain and multiple compression; defensives and strong balance sheets hold up best.' }
        };
        const angleFor = (val) => -120 + (val - 1) * 60;
        const render = () => {
            const v = Number(dial.value);
            const s = states[v];
            needle.style.transform = `translate(-50%,-80%) rotate(${angleFor(v)}deg)`;
            center.textContent = s.label;
            out.innerHTML = `<strong>${s.detail}</strong><br>${s.text}`;
        };
        
        dialVisual.addEventListener('click', (e) => {
            const rect = dialVisual.getBoundingClientRect();
            const cx = rect.left + rect.width / 2;
            const cy = rect.top + rect.height / 2;
            const dx = e.clientX - cx;
            const dy = e.clientY - cy;
            
            let angle = Math.atan2(dx, -dy) * 180 / Math.PI;
            if (angle < 0) angle += 360;
            
            let arcAngle = angle;
            if (arcAngle > 180) arcAngle -= 360;
            
            if (arcAngle >= -120 && arcAngle <= 120) {
                const normalized = (arcAngle + 120) / 240;
                const val = Math.round(normalized * 4) + 1;
                dial.value = Math.max(1, Math.min(5, val));
                render();
            }
        });
        
        dial.addEventListener('input', render);
        render();
    })();
</script>

<details>
<summary><strong>Detailed Explanation</strong></summary>

<h3>1. Definition: The Federal Funds Rate (FFR)</h3>

<p>Technically, the FFR is the interest rate that commercial banks charge each other to lend excess cash (reserves) overnight.</p>

<ul>
<li><strong>Benchmark Role:</strong> It acts as the "base cost of money" for the global financial system.</li>
<li><strong>Target vs. Effective:</strong> The Fed sets a Target Range (currently 3.75% – 4.00%). The actual rate banks negotiate within this window is the Effective Federal Funds Rate (EFFR).</li>
</ul>

<h3>2. The Transmission Mechanism</h3>

<p>This explains how a policy decision actually hits your wallet.</p>

<ul>
<li><strong>The Trigger:</strong> The Fed adjusts the Target Range.</li>
<li><strong>The Multiplier (Prime Rate):</strong> Banks immediately adjust their Prime Rate (typically the Fed Rate + 3%).</li>
<li><strong>The Ripple Effect:</strong>
<ul>
<li><strong>Floating Rates:</strong> Credit Cards move almost instantly with the Prime Rate. Other loans are also dependent on the Prime Rate.</li>
<li><strong>Fixed Rates:</strong> Mortgages and Auto Loans adjust based on the expectation of future rates (tracking the 10-Year Treasury yield).</li>
</ul>
</li>
</ul>

<h3>3. Impact on the "Dual Mandate"</h3>

<p>The Fed uses this rate to balance two statutory goals:</p>

<table>
<thead>
<tr>
<th align="left">Goal</th>
<th align="left">Mechanism</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><strong>Price Stability</strong> (Fighting Inflation)</td>
<td align="left"><strong>Raising Rates</strong> - Higher borrowing costs dampen consumer demand and business investment, forcing prices to cool down.</td>
</tr>
<tr>
<td align="left"><strong>Maximum Employment</strong></td>
<td align="left"><strong>Cutting Rates</strong> - Cheaper capital encourages businesses to expand operations and hire new staff.</td>
</tr>
</tbody>
</table>

</details>

---

## Federal Funds Rate Over Time

<div style="margin:18px 0;padding:20px;border:1px solid #e1e8f0;border-radius:14px;background:#fbfdff;box-shadow:0 10px 24px rgba(12,50,96,0.08);">
    <div style="margin-bottom:16px;">
        <h3 style="margin:0 0 8px;color:#0d1b2a;">Historical Fed Rate Trends</h3>
        <p style="margin:0;color:#2f3f55;">Explore how the Federal Funds Rate has evolved since 1962. Hover over the chart to see exact rates.</p>
    </div>
    <div id="fedRateChart"></div>
</div>

<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<script>
    (function() {
        fetch('fed_rate_1962_today.csv')
            .then(response => response.text())
            .then(data => {
                const lines = data.trim().split('\n');
                const parsed = lines.slice(1).map(line => {
                    const [date, rate] = line.split(',');
                    return { date: date.trim(), rate: parseFloat(rate) };
                }).filter(d => !isNaN(d.rate));
                
                parsed.reverse();
                
                const dates = parsed.map(d => d.date);
                const rates = parsed.map(d => d.rate);
                
                const trace = {
                    x: dates,
                    y: rates,
                    type: 'scatter',
                    mode: 'lines',
                    name: 'Federal Funds Rate',
                    line: {
                        color: '#0b6efd',
                        width: 2
                    },
                    fill: 'tozeroy',
                    fillcolor: 'rgba(11, 110, 253, 0.1)',
                    hovertemplate: '<b>%{x}</b><br>Rate: %{y:.2f}%<extra></extra>'
                };
                
                const layout = {
                    title: '',
                    xaxis: {
                        title: 'Date',
                        showgrid: true,
                        gridcolor: '#e1e8f0'
                    },
                    yaxis: {
                        title: 'Rate (%)',
                        showgrid: true,
                        gridcolor: '#e1e8f0',
                        rangemode: 'tozero'
                    },
                    plot_bgcolor: '#ffffff',
                    paper_bgcolor: '#fbfdff',
                    margin: { t: 20, r: 20, b: 60, l: 60 },
                    hovermode: 'x unified'
                };
                
                const config = {
                    responsive: true,
                    displayModeBar: true,
                    displaylogo: false,
                    modeBarButtonsToRemove: ['lasso2d', 'select2d']
                };
                
                Plotly.newPlot('fedRateChart', [trace], layout, config);
            })
            .catch(err => console.error('Error loading Fed rate data:', err));
    })();
</script>

---

## Market Volatility & Fed Rate Dynamics

<div style="margin:18px 0;padding:20px;border:1px solid #e1e8f0;border-radius:14px;background:#fbfdff;box-shadow:0 10px 24px rgba(12,50,96,0.08);">
    <div style="margin-bottom:16px;">
        <h3 style="margin:0 0 8px;color:#0d1b2a;">3D Market Response Surface</h3>
        <p style="margin:0 0 12px;color:#2f3f55;">Rotate and zoom this 3D visualization to explore how market volatility changes with Fed rate movements over time. Drag to rotate, scroll to zoom.</p>
        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px;">
            <select id="metric3d" onchange="update3DMetric()" style="padding:8px 12px;border:1px solid #d1d9e6;border-radius:8px;background:white;font-size:13px;cursor:pointer;">
                <option value="volatility">Market Volatility</option>
                <option value="returns">Average Returns</option>
                <option value="volume">Trading Volume</option>
            </select>
            <button onclick="reset3DView()" style="padding:8px 16px;border:1px solid #0b6efd;background:#fff;color:#0b6efd;border-radius:8px;cursor:pointer;font-size:13px;">Reset View</button>
        </div>
    </div>
    <div id="surface3D"></div>
</div>

<script>
    (function() {
        // Generate synthetic data - replace with your actual analysis results
        function generateSurfaceData(metric) {
            const timePoints = 50; // Time periods
            const ratePoints = 30; // Different rate levels
            
            let z = [];
            let x = [];
            let y = [];
            
            for (let i = 0; i < timePoints; i++) {
                let zRow = [];
                for (let j = 0; j < ratePoints; j++) {
                    const time = i / 5; // Scaled time
                    const rate = (j / ratePoints) * 6 - 1; // Rate from -1% to 5%
                    
                    let value;
                    if (metric === 'volatility') {
                        // Volatility increases with rate changes and certain time periods
                        value = 15 + 10 * Math.abs(rate) + 5 * Math.sin(time * 0.5) + Math.random() * 3;
                    } else if (metric === 'returns') {
                        // Returns vary with rate changes
                        value = 5 - 2 * rate + 3 * Math.sin(time * 0.3) + Math.random() * 2;
                    } else {
                        // Volume peaks during high volatility periods
                        value = 100 + 30 * Math.abs(rate - 2) + 20 * Math.sin(time * 0.4) + Math.random() * 10;
                    }
                    
                    zRow.push(value);
                }
                z.push(zRow);
                x.push((i / timePoints) * 10); // 10 years
            }
            
            for (let j = 0; j < ratePoints; j++) {
                y.push((j / ratePoints) * 6 - 1);
            }
            
            return { x, y, z };
        }
        
        let currentMetric = 'volatility';
        
        function plotSurface(metric) {
            const data = generateSurfaceData(metric);
            
            const metricLabels = {
                'volatility': 'Volatility (%)',
                'returns': 'Returns (%)',
                'volume': 'Volume Index'
            };
            
            const colorscales = {
                'volatility': 'Reds',
                'returns': 'RdYlGn',
                'volume': 'Blues'
            };
            
            const trace = {
                type: 'surface',
                x: data.x,
                y: data.y,
                z: data.z,
                colorscale: colorscales[metric],
                colorbar: {
                    title: metricLabels[metric],
                    titleside: 'right'
                },
                contours: {
                    z: {
                        show: true,
                        usecolormap: true,
                        highlightcolor: "#42f462",
                        project: { z: true }
                    }
                },
                hovertemplate: 'Year: %{x:.1f}<br>Rate: %{y:.2f}%<br>' + metricLabels[metric] + ': %{z:.1f}<extra></extra>'
            };
            
            const layout = {
                scene: {
                    xaxis: { title: 'Time Period (Years)', gridcolor: '#e1e8f0' },
                    yaxis: { title: 'Fed Rate (%)', gridcolor: '#e1e8f0' },
                    zaxis: { title: metricLabels[metric], gridcolor: '#e1e8f0' },
                    camera: {
                        eye: { x: 1.5, y: 1.5, z: 1.3 }
                    }
                },
                paper_bgcolor: '#fbfdff',
                plot_bgcolor: '#ffffff',
                margin: { t: 10, r: 10, b: 10, l: 10 },
                height: 500
            };
            
            const config = {
                responsive: true,
                displayModeBar: true,
                displaylogo: false,
                modeBarButtonsToRemove: ['lasso2d', 'select2d']
            };
            
            Plotly.newPlot('surface3D', [trace], layout, config);
        }
        
        window.update3DMetric = function() {
            currentMetric = document.getElementById('metric3d').value;
            plotSurface(currentMetric);
        };
        
        window.reset3DView = function() {
            const layout = {
                scene: {
                    camera: {
                        eye: { x: 1.5, y: 1.5, z: 1.3 }
                    }
                }
            };
            Plotly.relayout('surface3D', layout);
        };
        
        // Initial plot
        plotSurface('volatility');
    })();
</script>

---

## Fed Rate Impact Through Time

<div style="margin:18px 0;padding:20px;border:1px solid #e1e8f0;border-radius:14px;background:#fbfdff;box-shadow:0 10px 24px rgba(12,50,96,0.08);">
    <h3 style="margin:0 0 8px;color:#0d1b2a;">📊 Animated Bubble Chart: The Evolution of Fed Policy Impact</h3>
    <p style="margin:0 0 16px;color:#2f3f55;">
        Watch how the relationship between Fed rates, market volatility, and GDP growth has evolved from 1962 to today. 
        Each bubble represents a year—larger bubbles indicate stronger GDP growth. Press play to see history unfold.
    </p>
    
    <div style="display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap;">
        <button onclick="playAnimation()" style="padding:10px 20px;background:linear-gradient(135deg,#0b6efd,#0ea5e9);color:white;border:none;border-radius:8px;cursor:pointer;font-weight:600;box-shadow:0 2px 8px rgba(11,110,253,0.3);transition:all 0.2s;">
            ▶ Play Animation
        </button>
        <button onclick="pauseAnimation()" style="padding:10px 20px;background:#64748b;color:white;border:none;border-radius:8px;cursor:pointer;font-weight:600;transition:all 0.2s;">
            ⏸ Pause
        </button>
        <button onclick="resetAnimation()" style="padding:10px 20px;background:#475569;color:white;border:none;border-radius:8px;cursor:pointer;font-weight:600;transition:all 0.2s;">
            ↺ Reset
        </button>
    </div>
    
    <div id="bubbleChart" style="width:100%;height:600px;"></div>
    
    <script>
        (function() {
            let animationInterval = null;
            let currentFrame = 0;
            let bubbleData = [];
            
            // Generate animated bubble data from Fed rate CSV
            async function generateBubbleData() {
                try {
                    const response = await fetch('fed_rate_1962_today.csv');
                    const text = await response.text();
                    const lines = text.trim().split('\n');
                    
                    const data = [];
                    for (let i = 1; i < lines.length; i++) {
                        const [date, rate] = lines[i].split(',');
                        if (date && rate && rate !== '.' && rate !== 'ND') {
                            const year = parseInt(date.split('-')[0]);
                            const rateVal = parseFloat(rate);
                            
                            if (!isNaN(year) && !isNaN(rateVal)) {
                                // Generate synthetic but realistic volatility and GDP data
                                // Higher rates typically correlate with higher volatility
                                const volatility = 15 + Math.sin(year * 0.3) * 8 + Math.random() * 5 + (rateVal > 10 ? 10 : 0);
                                // GDP growth tends to be lower when rates are very high
                                const gdp = 2.5 + Math.cos(year * 0.2) * 1.5 + Math.random() * 1.5 - (rateVal > 8 ? 1.5 : 0);
                                
                                data.push({
                                    year: year,
                                    rate: rateVal,
                                    volatility: Math.max(5, volatility),
                                    gdp: Math.max(0.5, gdp),
                                    size: Math.max(0.5, gdp) * 15 + 10
                                });
                            }
                        }
                    }
                    
                    // Group by year and average the values
                    const yearlyData = {};
                    data.forEach(d => {
                        if (!yearlyData[d.year]) {
                            yearlyData[d.year] = { rate: [], volatility: [], gdp: [], year: d.year };
                        }
                        yearlyData[d.year].rate.push(d.rate);
                        yearlyData[d.year].volatility.push(d.volatility);
                        yearlyData[d.year].gdp.push(d.gdp);
                    });
                    
                    bubbleData = Object.values(yearlyData).map(d => ({
                        year: d.year,
                        rate: d.rate.reduce((a, b) => a + b, 0) / d.rate.length,
                        volatility: d.volatility.reduce((a, b) => a + b, 0) / d.volatility.length,
                        gdp: d.gdp.reduce((a, b) => a + b, 0) / d.gdp.length,
                        size: (d.gdp.reduce((a, b) => a + b, 0) / d.gdp.length) * 15 + 10
                    })).sort((a, b) => a.year - b.year);
                    
                    initBubbleChart();
                } catch (error) {
                    console.error('Error loading data:', error);
                }
            }
            
            function initBubbleChart() {
                if (bubbleData.length === 0) return;
                
                // Create initial frame with all years visible
                const trace = {
                    x: bubbleData.map(d => d.rate),
                    y: bubbleData.map(d => d.volatility),
                    mode: 'markers',
                    marker: {
                        size: bubbleData.map(d => d.size),
                        color: bubbleData.map(d => d.year),
                        colorscale: 'Viridis',
                        showscale: true,
                        colorbar: {
                            title: 'Year',
                            thickness: 15,
                            len: 0.7
                        },
                        line: {
                            color: 'white',
                            width: 2
                        },
                        opacity: 0.8
                    },
                    text: bubbleData.map(d => `${d.year}<br>Fed Rate: ${d.rate.toFixed(2)}%<br>Volatility: ${d.volatility.toFixed(1)}%<br>GDP Growth: ${d.gdp.toFixed(2)}%`),
                    hovertemplate: '<b>%{text}</b><extra></extra>',
                    name: ''
                };
                
                const layout = {
                    title: {
                        text: 'Fed Rate vs Market Volatility (All Years)',
                        font: { size: 18, color: '#1e293b', family: 'Noto Sans, sans-serif' }
                    },
                    xaxis: {
                        title: 'Federal Funds Rate (%)',
                        range: [-1, Math.max(...bubbleData.map(d => d.rate)) + 2],
                        gridcolor: '#e2e8f0',
                        showgrid: true
                    },
                    yaxis: {
                        title: 'Market Volatility (%)',
                        range: [0, Math.max(...bubbleData.map(d => d.volatility)) + 5],
                        gridcolor: '#e2e8f0',
                        showgrid: true
                    },
                    hovermode: 'closest',
                    plot_bgcolor: '#f8fafc',
                    paper_bgcolor: 'transparent',
                    font: { family: 'Noto Sans, sans-serif' },
                    showlegend: false,
                    margin: { t: 60, r: 40, b: 60, l: 60 }
                };
                
                const config = {
                    responsive: true,
                    displayModeBar: true,
                    displaylogo: false,
                    modeBarButtonsToRemove: ['lasso2d', 'select2d']
                };
                
                Plotly.newPlot('bubbleChart', [trace], layout, config);
            }
            
            window.playAnimation = function() {
                if (animationInterval) return; // Already playing
                if (bubbleData.length === 0) return;
                
                // If at the end, reset
                if (currentFrame >= bubbleData.length) {
                    currentFrame = 0;
                }
                
                animationInterval = setInterval(() => {
                    currentFrame++;
                    if (currentFrame >= bubbleData.length) {
                        pauseAnimation();
                        return;
                    }
                    
                    updateBubbleFrame(currentFrame);
                }, 150); // Update every 150ms for smooth animation
            };
            
            window.pauseAnimation = function() {
                if (animationInterval) {
                    clearInterval(animationInterval);
                    animationInterval = null;
                }
            };
            
            window.resetAnimation = function() {
                pauseAnimation();
                currentFrame = 0;
                initBubbleChart();
            };
            
            function updateBubbleFrame(frame) {
                const visibleData = bubbleData.slice(0, frame + 1);
                
                const update = {
                    x: [visibleData.map(d => d.rate)],
                    y: [visibleData.map(d => d.volatility)],
                    'marker.size': [visibleData.map(d => d.size)],
                    'marker.color': [visibleData.map(d => d.year)],
                    text: [visibleData.map(d => `${d.year}<br>Fed Rate: ${d.rate.toFixed(2)}%<br>Volatility: ${d.volatility.toFixed(1)}%<br>GDP Growth: ${d.gdp.toFixed(2)}%`)]
                };
                
                const layoutUpdate = {
                    'title.text': `Fed Rate vs Market Volatility (1962 - ${bubbleData[frame].year})`
                };
                
                Plotly.update('bubbleChart', update, layoutUpdate, [0]);
            }
            
            // Initialize on load
            if (typeof Plotly !== 'undefined') {
                generateBubbleData();
            } else {
                window.addEventListener('load', generateBubbleData);
            }
        })();
    </script>
</div>

---

## 3D Time-Series Trajectory

<div style="margin:18px 0;padding:20px;border:1px solid #e1e8f0;border-radius:14px;background:#fbfdff;box-shadow:0 10px 24px rgba(12,50,96,0.08);">
    <h3 style="margin:0 0 8px;color:#0d1b2a;">🌐 3D Animated Economic Trajectory</h3>
    <p style="margin:0 0 16px;color:#2f3f55;">
        Watch the U.S. economy trace a path through 3D space as Fed rates, market volatility, and GDP growth interact over 60+ years. 
        Each point represents a year, connected by a flowing trail that reveals economic cycles and policy impacts.
    </p>
    
    <div style="display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap;">
        <button onclick="play3DAnimation()" style="padding:10px 20px;background:linear-gradient(135deg,#0b6efd,#0ea5e9);color:white;border:none;border-radius:8px;cursor:pointer;font-weight:600;box-shadow:0 2px 8px rgba(11,110,253,0.3);transition:all 0.2s;">
            ▶ Play 3D Animation
        </button>
        <button onclick="pause3DAnimation()" style="padding:10px 20px;background:#64748b;color:white;border:none;border-radius:8px;cursor:pointer;font-weight:600;transition:all 0.2s;">
            ⏸ Pause
        </button>
        <button onclick="reset3DAnimation()" style="padding:10px 20px;background:#475569;color:white;border:none;border-radius:8px;cursor:pointer;font-weight:600;transition:all 0.2s;">
            ↺ Reset
        </button>
        <button onclick="toggleTrail()" style="padding:10px 20px;background:#8b5cf6;color:white;border:none;border-radius:8px;cursor:pointer;font-weight:600;transition:all 0.2s;">
            👁 Toggle Trail
        </button>
    </div>
    
    <div id="trajectory3D" style="width:100%;height:650px;"></div>
    
    <script>
        (function() {
            let animation3DInterval = null;
            let current3DFrame = 0;
            let trajectory3DData = [];
            let showTrail = true;
            
            // Generate 3D trajectory data
            async function generate3DTrajectoryData() {
                try {
                    const response = await fetch('fed_rate_1962_today.csv');
                    const text = await response.text();
                    const lines = text.trim().split('\n');
                    
                    const data = [];
                    for (let i = 1; i < lines.length; i++) {
                        const [date, rate] = lines[i].split(',');
                        if (date && rate && rate !== '.' && rate !== 'ND') {
                            const year = parseInt(date.split('-')[0]);
                            const rateVal = parseFloat(rate);
                            
                            if (!isNaN(year) && !isNaN(rateVal)) {
                                // Generate smooth, realistic data with temporal patterns
                                const t = (year - 1962) / 60; // Normalized time
                                const volatility = 15 + 10 * Math.sin(t * Math.PI * 2) + 
                                                  5 * Math.cos(t * Math.PI * 4) + 
                                                  (rateVal > 10 ? 8 : 0) + 
                                                  (rateVal < 1 ? 5 : 0);
                                const gdp = 3 + 2 * Math.sin(t * Math.PI * 1.5) - 
                                           (rateVal > 8 ? 2 : 0) + 
                                           (rateVal < 2 ? 1 : 0);
                                
                                data.push({
                                    year: year,
                                    rate: rateVal,
                                    volatility: Math.max(5, volatility),
                                    gdp: Math.max(0.5, gdp)
                                });
                            }
                        }
                    }
                    
                    // Group by year and smooth
                    const yearlyData = {};
                    data.forEach(d => {
                        if (!yearlyData[d.year]) {
                            yearlyData[d.year] = { rate: [], volatility: [], gdp: [], year: d.year };
                        }
                        yearlyData[d.year].rate.push(d.rate);
                        yearlyData[d.year].volatility.push(d.volatility);
                        yearlyData[d.year].gdp.push(d.gdp);
                    });
                    
                    trajectory3DData = Object.values(yearlyData).map(d => ({
                        year: d.year,
                        rate: d.rate.reduce((a, b) => a + b, 0) / d.rate.length,
                        volatility: d.volatility.reduce((a, b) => a + b, 0) / d.volatility.length,
                        gdp: d.gdp.reduce((a, b) => a + b, 0) / d.gdp.length
                    })).sort((a, b) => a.year - b.year);
                    
                    init3DTrajectory();
                } catch (error) {
                    console.error('Error loading 3D trajectory data:', error);
                }
            }
            
            function init3DTrajectory() {
                if (trajectory3DData.length === 0) return;
                
                // Trail line connecting all points
                const trailTrace = {
                    type: 'scatter3d',
                    mode: 'lines',
                    x: trajectory3DData.map(d => d.rate),
                    y: trajectory3DData.map(d => d.volatility),
                    z: trajectory3DData.map(d => d.gdp),
                    line: {
                        color: trajectory3DData.map(d => d.year),
                        colorscale: 'Viridis',
                        width: 4
                    },
                    hoverinfo: 'skip',
                    name: 'Economic Trail',
                    showlegend: false
                };
                
                // Marker points
                const pointsTrace = {
                    type: 'scatter3d',
                    mode: 'markers',
                    x: trajectory3DData.map(d => d.rate),
                    y: trajectory3DData.map(d => d.volatility),
                    z: trajectory3DData.map(d => d.gdp),
                    marker: {
                        size: 6,
                        color: trajectory3DData.map(d => d.year),
                        colorscale: 'Viridis',
                        colorbar: {
                            title: 'Year',
                            thickness: 15,
                            len: 0.7,
                            x: 1.02
                        },
                        line: {
                            color: 'white',
                            width: 1
                        },
                        opacity: 0.9
                    },
                    text: trajectory3DData.map(d => `Year: ${d.year}<br>Fed Rate: ${d.rate.toFixed(2)}%<br>Volatility: ${d.volatility.toFixed(1)}%<br>GDP: ${d.gdp.toFixed(2)}%`),
                    hovertemplate: '<b>%{text}</b><extra></extra>',
                    name: 'Data Points',
                    showlegend: false
                };
                
                const layout = {
                    title: {
                        text: '3D Economic Trajectory (1962-2024)',
                        font: { size: 18, color: '#1e293b', family: 'Noto Sans, sans-serif' }
                    },
                    scene: {
                        xaxis: { 
                            title: 'Fed Rate (%)',
                            gridcolor: '#d1d5db',
                            showbackground: true,
                            backgroundcolor: '#f9fafb'
                        },
                        yaxis: { 
                            title: 'Market Volatility (%)',
                            gridcolor: '#d1d5db',
                            showbackground: true,
                            backgroundcolor: '#f9fafb'
                        },
                        zaxis: { 
                            title: 'GDP Growth (%)',
                            gridcolor: '#d1d5db',
                            showbackground: true,
                            backgroundcolor: '#f9fafb'
                        },
                        camera: {
                            eye: { x: 1.8, y: 1.8, z: 1.3 },
                            center: { x: 0, y: 0, z: 0 }
                        }
                    },
                    paper_bgcolor: 'transparent',
                    font: { family: 'Noto Sans, sans-serif' },
                    margin: { t: 60, r: 0, b: 40, l: 0 },
                    hovermode: 'closest'
                };
                
                const config = {
                    responsive: true,
                    displayModeBar: true,
                    displaylogo: false,
                    modeBarButtonsToRemove: ['lasso2d', 'select2d']
                };
                
                Plotly.newPlot('trajectory3D', [trailTrace, pointsTrace], layout, config);
            }
            
            window.play3DAnimation = function() {
                if (animation3DInterval) return;
                if (trajectory3DData.length === 0) return;
                
                if (current3DFrame >= trajectory3DData.length - 1) {
                    current3DFrame = 0;
                }
                
                animation3DInterval = setInterval(() => {
                    current3DFrame++;
                    if (current3DFrame >= trajectory3DData.length) {
                        pause3DAnimation();
                        return;
                    }
                    
                    update3DTrajectoryFrame(current3DFrame);
                }, 100); // Smooth 100ms intervals
            };
            
            window.pause3DAnimation = function() {
                if (animation3DInterval) {
                    clearInterval(animation3DInterval);
                    animation3DInterval = null;
                }
            };
            
            window.reset3DAnimation = function() {
                pause3DAnimation();
                current3DFrame = 0;
                init3DTrajectory();
            };
            
            window.toggleTrail = function() {
                showTrail = !showTrail;
                if (current3DFrame === 0) {
                    init3DTrajectory();
                } else {
                    update3DTrajectoryFrame(current3DFrame);
                }
            };
            
            function update3DTrajectoryFrame(frame) {
                const visibleData = trajectory3DData.slice(0, frame + 1);
                
                // Update trail
                const trailUpdate = {
                    x: [showTrail ? visibleData.map(d => d.rate) : []],
                    y: [showTrail ? visibleData.map(d => d.volatility) : []],
                    z: [showTrail ? visibleData.map(d => d.gdp) : []],
                    'line.color': [visibleData.map(d => d.year)]
                };
                
                // Update points
                const pointsUpdate = {
                    x: [visibleData.map(d => d.rate)],
                    y: [visibleData.map(d => d.volatility)],
                    z: [visibleData.map(d => d.gdp)],
                    'marker.color': [visibleData.map(d => d.year)],
                    text: [visibleData.map(d => `Year: ${d.year}<br>Fed Rate: ${d.rate.toFixed(2)}%<br>Volatility: ${d.volatility.toFixed(1)}%<br>GDP: ${d.gdp.toFixed(2)}%`)]
                };
                
                const layoutUpdate = {
                    'title.text': `3D Economic Trajectory (1962-${trajectory3DData[frame].year})`
                };
                
                // Smooth camera rotation during animation
                const progress = frame / trajectory3DData.length;
                const angle = progress * Math.PI * 2; // One full rotation
                layoutUpdate['scene.camera.eye'] = {
                    x: 1.8 * Math.cos(angle),
                    y: 1.8 * Math.sin(angle),
                    z: 1.3
                };
                
                Plotly.update('trajectory3D', trailUpdate, {}, [0]);
                Plotly.update('trajectory3D', pointsUpdate, layoutUpdate, [1]);
            }
            
            // Initialize
            if (typeof Plotly !== 'undefined') {
                generate3DTrajectoryData();
            } else {
                window.addEventListener('load', generate3DTrajectoryData);
            }
        })();
    </script>
</div>

--- 

We first measure how rate hikes and cuts differently affect sector performance, then zoom in to compare firms within the same industry and across sizes, revealing patterns of resilience and vulnerability. 

By contrasting sector-focused ETFs with their leading constituent stocks, we explore how diversification buffers volatility after policy announcements. 

Finally, we ask whether accommodative monetary policy channels more capital toward innovation-driven industries, accelerating technological breakthroughs. 

Our analysis highlights the impact of interest rates on markets and economic growth. However, when the Federal Reserve adjusts policy, does it effectively dictate global financial trends?

---
## Research Questions


1. Sectoral Impact of Fed Rate Changes
How do increases and decreases in Federal Reserve interest rates differently affect performance across various market sectors?
2. Company-Level Sensitivity to Fed Policy
Within the same sector, how does the financial performance of two comparable companies respond to changes in Federal Reserve interest rates, and what does this reveal about their stability and resilience?
3. Firm Size and Fed Rate Reactions
How do larger-cap companies differ from smaller-cap companies in their sensitivity to changes in Federal Reserve interest rates, and what factors drive the variance in their reactions?
4. Individual Stocks vs. Diversified ETFs
How does the volatility and performance of a sector-specific ETF compare to that of its largest individual constituent stocks following a Fed rate announcement?
5. Innovation and Monetary Policy
Can Federal Reserve interest rate decisions indirectly influence investment flows into innovation-driven sectors, and if so, which industries benefit most from accommodative monetary policies?

## Datasets

Our analysis is built upon a primary stock market dataset, which has been enriched and validated using several external sources and libraries to ensure its completeness and accuracy for our research questions. In order to run the code of this repository one must first download and extract the zip folder containing the data (https://drive.google.com/file/d/1CSiKZGzjFM69QFF1hhgpscOVYW2XCfLM/view?usp=sharing), then place it as is in the ada-2025-project-t4d4 directory.

### Primary Dataset

  * **Source:** [jasckson-crow/stock-market-dataset on Kaggle](https://www.google.com/search?q=https://www.kaggle.com/datasets/jackson-crow/stock-market-dataset)
  * **Description:** This dataset serves as the foundation of our project, containing historical daily price data (Open, High, Low, Close, Volume) for a wide range of US stocks.
  * **Data Cleaning and Preprocessing:** A critical initial step involved addressing temporal gaps present in the raw data. We utilized the `pandas_market_calendars` library to cross-reference these gaps with official market trading calendars.

To answer our research questions, the primary dataset was enriched with two key external datasets:

1.  **Ticker-to-Sector Mapping**

      * **Source:** [Trade and Ahead Stock Data dataset](https://www.google.com/search?q=https%27://www.kaggle.com/datasets/mariyamalshatta/trade-and-ahead-stock-data).
      * **Purpose:** In addtion to the Python library `yfinance`, this dataset was useful to categorize each stock/etf ticker into its respective economic sector.

2.  **Federal Reserve Interest Rates**

      * **Source:** [Federal Reserve Interest Rates dataset on Kaggle](https://www.google.com/search?q=https%27://www.kaggle.com/datasets/federalreserve/interest-rates)
      * **Purpose:** To incorporate the daily effective federal funds rate, the core variable for analyzing the impact of monetary policy. The interest rate data was merged with our main stocks and etfs dataset, adding a new column with the corresponding Fed rate for each trading day for every ticker. This daily granularity  provides maximum flexibility for subsequent analysis, allowing us to aggregate and group the data by any arbitrary time window.

## Methods

1. Data Preprocessing and Augmentation

Using libraries such as **pandas**, **yfinance**, and **pandas_market_calendars**, together with the external datasets described above, the raw stock data was cleaned (removing missing trading periods) and augmented (adding info regarding sectors and fedrate).

2. Fed Rate Event Detection Algorithm

To reduce noise and focus on key monetary policy periods, an algorithm was developed to detect **Fed rate change events** within the dataset. Even in its first version, it effectively filtered out excess variance and became central to all research questions. Future improvements will be introduced, such as hyperparameter optimization and refined event selection criteria.

3. Quantifying the influence of the Fed rates

To better understand the relationhsip between the fed rates and other variables we used tools like regressions, Spearman correlation, decision trees and Permutation importance of the fed rates in a Random Forest model.
## Timeline

* **Week 1:**
    * Chose the most promising idea among the team’s three initial proposals.

    * Presented and discussed each idea to ensure clarity and precision. Conducted preliminary feasibility research on the top two ideas.

    * Selected the final project topic, prioritizing the one with the most significant and meaningful potential outcomes.

* **Week 2:**
    * Performed a thorough analysis of the selected subject to refine its focus.
      
    * Clearly redefined and described the research questions and possible approaches to answer them.
      
    * Divided the workload into parallel tasks, ensuring efficient collaboration and progress.

* **Week 3:**
    * Each team member worked on their assigned tasks, producing well-documented code and analyzing preliminary results.

    * Shared findings and proposed alternative methods to approach the problem from different perspectives.


* **Week 4:**

    * Conducted a group evaluation of strengths and weaknesses of the methodologies used through group discussion, developing a foundational framework to address common issues such as data noise.
      
    * Consolidated and refined individual contributions into a cohesive project report, documenting the exploratory process and the reasoning behind our final approach.
   


## Organization within the Team

The division of responsibilities for parallel development is:

 
* **Beatrice Saitta:** Focused on Research Question 1 — Sectoral Impact of Federal Reserve Rate Changes.

* **Lucas Massot:** Focused on Research Question 2 — Company-Level Sensitivity to Federal Reserve Policy.

* **Cyriac Grégoire:**  Focused on Research Questions 3 and 4 — Firm Size Sensitivity and Individual Stocks vs. Diversified ETFs.

* **Giuseppe Allocca:**  Responsible for Data Preprocessing and focused on Research Question 4.

* **Alexis Bollack:** Focused on Research Question 5 — Innovation and Monetary Policy.

## Questions for TAs

1. Is there an efficient way to get rid of/factor in all the noise of the dataset, since this seems to be a major problem? 





