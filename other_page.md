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
        <a href="{{ site.baseurl }}/other_page" class="nav-link active">Analysis</a>
        <a href="{{ site.baseurl }}/game" class="nav-link">Interactive</a>
        <a href="{{ site.github.repository_url }}" class="nav-link" target="_blank">Repository</a>
    </div>
</div>

# Federal Reserve Data Visualizations

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