<style>
/* Top navigation bar */
.top-nav {
    background: #000;
    border-bottom: 1px solid #333;
    position: relative;
    left: -90px;
    width: calc(100% + 180px);
    padding: 0;
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
/* Black header with title */
.header-black {
    background: #000;
    color: #fff;
    padding: 20px 0;
    margin: 0 0 0 0;
    position: relative;
    left: -90px;
    width: calc(100% + 180px);
}
.header-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 40px;
}
.header-title {
    font-size: 32px;
    font-weight: 700;
    color: #fff;
    margin: 0;
    letter-spacing: -0.5px;
    flex: 1;
}
.header-fed-rate {
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 16px 24px;
    background: #1a1a1a;
    border-radius: 6px;
    border: 1px solid #333;
}
.fed-rate-info {
    display: flex;
    flex-direction: column;
    gap: 4px;
}
.fed-rate-label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: #999;
    font-weight: 600;
}
.fed-rate-value {
    font-size: 28px;
    font-weight: 700;
    color: #fff;
    line-height: 1;
}
.fed-rate-change {
    font-size: 12px;
    color: #00d084;
    font-weight: 600;
}
.fed-rate-chart {
    width: 165px;
    height: 60px;
    position: relative;
    background: #0a0a0a;
    border-radius: 4px;
    padding: 8px 8px 8px 24px;
}
.fed-rate-chart svg {
    width: 100%;
    height: 100%;
}
.chart-axis-label {
    font-size: 9px;
    fill: #666;
    font-weight: 500;
}
/* Bloomberg-style market ticker */
.market-ticker-wrapper {
    background: #000;
    color: #fff;
    padding: 0;
    margin: 0 0 30px 0;
    overflow: hidden;
    border-bottom: 1px solid #1a1a1a;
    position: relative;
    left: -90px;
    width: calc(100% + 180px);
}
.market-ticker {
    display: flex;
    animation: scroll-ticker 60s linear infinite;
    white-space: nowrap;
    padding: 12px 0;
}
.ticker-item {
    display: inline-flex;
    align-items: center;
    padding: 0 32px;
    gap: 16px;
    border-right: 1px solid #333;
    font-size: 14px;
    font-weight: 500;
}
.ticker-symbol {
    font-weight: 700;
    font-size: 13px;
    letter-spacing: 0.5px;
    margin-right: 4px;
}
.ticker-price {
    font-weight: 600;
    font-size: 14px;
    margin-left: 4px;
}
.ticker-change {
    font-size: 13px;
    padding: 2px 6px;
    border-radius: 3px;
}
.ticker-change.positive {
    color: #00d084;
    background: rgba(0, 208, 132, 0.1);
}
.ticker-change.negative {
    color: #ff4757;
    background: rgba(255, 71, 87, 0.1);
}
@keyframes scroll-ticker {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}
.pulse {
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}
</style>

<div class="top-nav">
    <div class="top-nav-content">
        <a href="{{ site.baseurl }}/" class="nav-link active">Home</a>
        <a href="{{ site.baseurl }}/other_page" class="nav-link">Analysis</a>
        <a href="{{ site.baseurl }}/game" class="nav-link">Game</a>
        <a href="{{ site.baseurl }}/Beatrice" class="nav-link">Beatrice</a>
        <a href="{{ site.baseurl }}/Cyriac" class="nav-link">Cyriac</a>
        <a href="{{ site.baseurl }}/Lucas" class="nav-link">Lucas</a>
        <a href="{{ site.baseurl }}/Alexis" class="nav-link">Alexis</a>
        <a href="{{ site.github.repository_url }}" class="nav-link" target="_blank">Repository</a>
    </div>
</div>

<div class="header-black">
    <div class="header-content">
        <h1 class="header-title">Is Washington truly conducting the symphony of global finance?</h1>
        <div class="header-fed-rate">
            <div class="fed-rate-info">
                <div class="fed-rate-label">Federal Funds Rate</div>
                <div class="fed-rate-value" id="header-fed-rate">4.33%</div>
                <div class="fed-rate-change" id="header-fed-change">↑ 0.25 (Last meeting)</div>
            </div>
            <div class="fed-rate-chart">
                <svg viewBox="-30 0 170 60" preserveAspectRatio="none">
                    <!-- Grid lines -->
                    <line x1="0" y1="12" x2="140" y2="12" stroke="#333" stroke-width="0.5" opacity="0.3"/>
                    <line x1="0" y1="24" x2="140" y2="24" stroke="#333" stroke-width="0.5" opacity="0.3"/>
                    <line x1="0" y1="36" x2="140" y2="36" stroke="#333" stroke-width="0.5" opacity="0.3"/>
                    <!-- Area fill -->
                    <path
                        id="fed-rate-area"
                        fill="url(#gradient)"
                        d="M0,42 L11.67,40 L23.33,37 L35,35 L46.67,32 L58.33,28 L70,25 L81.67,22 L93.33,19 L105,16 L116.67,14 L128.33,12 L140,10 L140,48 L0,48 Z"
                    />
                    <!-- Line chart -->
                    <polyline
                        id="fed-rate-sparkline"
                        fill="none"
                        stroke="#00d084"
                        stroke-width="2.5"
                        stroke-linecap="round"
                        points="0,42 11.67,40 23.33,37 35,35 46.67,32 58.33,28 70,25 81.67,22 93.33,19 105,16 116.67,14 128.33,12 140,10"
                    />
                    <!-- Y-axis labels -->
                    <text x="-30" y="12" class="chart-axis-label" text-anchor="start" id="y-label-high">5.5%</text>
                    <text x="-30" y="36" class="chart-axis-label" text-anchor="start" id="y-label-low">4.0%</text>
                    <!-- Time axis labels -->
                    <text x="0" y="58" class="chart-axis-label">2023</text>
                    <text x="70" y="58" class="chart-axis-label" text-anchor="middle">2024</text>
                    <text x="140" y="58" class="chart-axis-label" text-anchor="end">2025</text>
                    <!-- Gradient definition -->
                    <defs>
                        <linearGradient id="gradient" x1="0%" y1="0%" x2="0%" y2="100%">
                            <stop offset="0%" style="stop-color:#00d084;stop-opacity:0.3" />
                            <stop offset="100%" style="stop-color:#00d084;stop-opacity:0" />
                        </linearGradient>
                    </defs>
                </svg>
            </div>
        </div>
    </div>
</div>

<div class="market-ticker-wrapper">
    <div class="market-ticker" id="market-ticker">
        <!-- First set of tickers -->
        <div class="ticker-item">
            <span class="ticker-symbol">FED RATE</span>
            <span class="ticker-price" id="fed-rate">4.33%</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-symbol">S&P 500</span>
            <span class="ticker-price" id="sp500">6,051.09</span>
            <span class="ticker-change positive" id="sp500-change">+0.82%</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-symbol">DOW</span>
            <span class="ticker-price" id="dow">43,988.99</span>
            <span class="ticker-change negative" id="dow-change">-0.22%</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-symbol">NASDAQ</span>
            <span class="ticker-price" id="nasdaq">19,478.88</span>
            <span class="ticker-change positive" id="nasdaq-change">+1.24%</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-symbol">AAPL</span>
            <span class="ticker-price" id="aapl">245.18</span>
            <span class="ticker-change positive" id="aapl-change">+1.12%</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-symbol">MSFT</span>
            <span class="ticker-price" id="msft">441.58</span>
            <span class="ticker-change positive" id="msft-change">+0.76%</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-symbol">GOOGL</span>
            <span class="ticker-price" id="googl">198.45</span>
            <span class="ticker-change negative" id="googl-change">-0.34%</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-symbol">AMZN</span>
            <span class="ticker-price" id="amzn">227.89</span>
            <span class="ticker-change positive" id="amzn-change">+1.89%</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-symbol">TSLA</span>
            <span class="ticker-price" id="tsla">412.67</span>
            <span class="ticker-change positive" id="tsla-change">+2.34%</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-symbol">META</span>
            <span class="ticker-price" id="meta">638.42</span>
            <span class="ticker-change negative" id="meta-change">-0.91%</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-symbol">NVDA</span>
            <span class="ticker-price" id="nvda">145.32</span>
            <span class="ticker-change positive" id="nvda-change">+3.21%</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-symbol">JPM</span>
            <span class="ticker-price" id="jpm">258.73</span>
            <span class="ticker-change positive" id="jpm-change">+0.54%</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-symbol">GOLD</span>
            <span class="ticker-price" id="gold">2,689.50</span>
            <span class="ticker-change positive" id="gold-change">+0.45%</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-symbol">OIL</span>
            <span class="ticker-price" id="oil">71.23</span>
            <span class="ticker-change negative" id="oil-change">-1.12%</span>
        </div>
        <!-- Duplicate for seamless loop -->
        <div class="ticker-item">
            <span class="ticker-symbol">FED RATE</span>
            <span class="ticker-price">4.33%</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-symbol">S&P 500</span>
            <span class="ticker-price">6,051.09</span>
            <span class="ticker-change positive">+0.82%</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-symbol">DOW</span>
            <span class="ticker-price">43,988.99</span>
            <span class="ticker-change negative">-0.22%</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-symbol">NASDAQ</span>
            <span class="ticker-price">19,478.88</span>
            <span class="ticker-change positive">+1.24%</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-symbol">AAPL</span>
            <span class="ticker-price">245.18</span>
            <span class="ticker-change positive">+1.12%</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-symbol">MSFT</span>
            <span class="ticker-price">441.58</span>
            <span class="ticker-change positive">+0.76%</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-symbol">GOOGL</span>
            <span class="ticker-price">198.45</span>
            <span class="ticker-change negative">-0.34%</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-symbol">AMZN</span>
            <span class="ticker-price">227.89</span>
            <span class="ticker-change positive">+1.89%</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-symbol">TSLA</span>
            <span class="ticker-price">412.67</span>
            <span class="ticker-change positive">+2.34%</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-symbol">META</span>
            <span class="ticker-price">638.42</span>
            <span class="ticker-change negative">-0.91%</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-symbol">NVDA</span>
            <span class="ticker-price">145.32</span>
            <span class="ticker-change positive">+3.21%</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-symbol">JPM</span>
            <span class="ticker-price">258.73</span>
            <span class="ticker-change positive">+0.54%</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-symbol">GOLD</span>
            <span class="ticker-price">2,689.50</span>
            <span class="ticker-change positive">+0.45%</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-symbol">OIL</span>
            <span class="ticker-price">71.23</span>
            <span class="ticker-change negative">-1.12%</span>
        </div>
    </div>
</div>

<script>
(function() {
    // Stock ticker simulation
    const stocks = [
        { id: 'sp500', base: 6051.09, variance: 50 },
        { id: 'dow', base: 43988.99, variance: 200 },
        { id: 'nasdaq', base: 19478.88, variance: 150 },
        { id: 'aapl', base: 245.18, variance: 3 },
        { id: 'msft', base: 441.58, variance: 5 },
        { id: 'googl', base: 198.45, variance: 2 },
        { id: 'amzn', base: 227.89, variance: 3 },
        { id: 'tsla', base: 412.67, variance: 8 },
        { id: 'meta', base: 638.42, variance: 7 },
        { id: 'nvda', base: 145.32, variance: 4 },
        { id: 'jpm', base: 258.73, variance: 3 },
        { id: 'gold', base: 2689.50, variance: 15 },
        { id: 'oil', base: 71.23, variance: 1.5 }
    ];
    
    function updateStock(stock) {
        const priceEl = document.getElementById(stock.id);
        const changeEl = document.getElementById(stock.id + '-change');
        
        if (!priceEl || !changeEl) return;
        
        const variance = (Math.random() - 0.5) * stock.variance * 2;
        const newValue = stock.base + variance;
        const changePercent = ((variance / stock.base) * 100).toFixed(2);
        const isPositive = variance >= 0;
        
        priceEl.textContent = newValue.toFixed(2);
        changeEl.textContent = `${isPositive ? '+' : ''}${changePercent}%`;
        changeEl.className = `ticker-change ${isPositive ? 'positive' : 'negative'}`;
    }
    
    // Update all stocks every 4 seconds
    setInterval(() => {
        stocks.forEach(stock => updateStock(stock));
    }, 4000);
    
    // Micro-updates for individual stocks every second (more realistic)
    setInterval(() => {
        const randomStock = stocks[Math.floor(Math.random() * stocks.length)];
        updateStock(randomStock);
    }, 1000);
    
    // Load real Fed Rate data and update chart
    fetch('fed_rate_1962_today.csv')
        .then(response => response.text())
        .then(data => {
            const lines = data.trim().split('\n');
            const parsed = lines.slice(1).map(line => {
                const [date, rate] = line.split(',');
                return { date: date.trim(), rate: parseFloat(rate) };
            }).filter(d => !isNaN(d.rate));
            
            // Filter for 2023-01-01 to today
            const since2023 = parsed.filter(d => d.date >= '2023-01-01');
            since2023.reverse(); // oldest to newest
            
            if (since2023.length === 0) return;
            
            // Update current rate display
            const latestRate = parsed[0].rate;
            const headerRateEl = document.getElementById('header-fed-rate');
            const tickerRateEl = document.getElementById('fed-rate');
            if (headerRateEl) headerRateEl.textContent = latestRate.toFixed(2) + '%';
            if (tickerRateEl) tickerRateEl.textContent = latestRate.toFixed(2) + '%';
            
            // Calculate rate change
            const oldestRate = since2023[0].rate;
            const rateChange = latestRate - oldestRate;
            const changeEl = document.getElementById('header-fed-change');
            if (changeEl) {
                const arrow = rateChange >= 0 ? '↑' : '↓';
                changeEl.textContent = `${arrow} ${Math.abs(rateChange).toFixed(2)} (Since 2023)`;
                changeEl.style.color = rateChange >= 0 ? '#00d084' : '#ff4757';
            }
            
            // Update SVG chart with real data
            const svgWidth = 140;
            const svgHeight = 48;
            const padding = 4;
            
            // Find min/max for scaling
            const rates = since2023.map(d => d.rate);
            const minRate = Math.min(...rates);
            const maxRate = Math.max(...rates);
            const rateRange = maxRate - minRate || 1;
            
            // Create points for the chart
            const points = since2023.map((d, i) => {
                const x = (i / (since2023.length - 1)) * svgWidth;
                const y = svgHeight - padding - ((d.rate - minRate) / rateRange) * (svgHeight - 2 * padding);
                return `${x.toFixed(2)},${y.toFixed(2)}`;
            }).join(' ');
            
            // Create area path
            const areaPath = `M0,${svgHeight - padding} L` + 
                since2023.map((d, i) => {
                    const x = (i / (since2023.length - 1)) * svgWidth;
                    const y = svgHeight - padding - ((d.rate - minRate) / rateRange) * (svgHeight - 2 * padding);
                    return `${x.toFixed(2)},${y.toFixed(2)}`;
                }).join(' L') + 
                ` L${svgWidth},${svgHeight} L0,${svgHeight} Z`;
            
            // Update the polyline and area
            const sparkline = document.getElementById('fed-rate-sparkline');
            const areaFill = document.getElementById('fed-rate-area');
            
            if (sparkline) sparkline.setAttribute('points', points);
            if (areaFill) areaFill.setAttribute('d', areaPath);
            
            // Update Y-axis labels with actual min/max values
            const yLabelHigh = document.getElementById('y-label-high');
            const yLabelLow = document.getElementById('y-label-low');
            if (yLabelHigh) yLabelHigh.textContent = maxRate.toFixed(1) + '%';
            if (yLabelLow) yLabelLow.textContent = minRate.toFixed(1) + '%';
            
            // Update color based on trend
            const isIncreasing = latestRate > oldestRate;
            const color = isIncreasing ? '#00d084' : '#ff4757';
            if (sparkline) sparkline.setAttribute('stroke', color);
            
            // Update gradient
            const gradient = document.querySelector('#gradient stop:first-child');
            if (gradient) gradient.setAttribute('style', `stop-color:${color};stop-opacity:0.3`);
        })
        .catch(err => console.error('Error loading Fed Rate data:', err));
})();
</script>
  
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





