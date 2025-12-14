import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'helpers'))

import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import argparse
from fed_events_analysis import identify_fed_rate_signals, plot_fed_rate_overview

# Command-line argument parser
parser = argparse.ArgumentParser(description='Generate Fed rate signal graphs with customizable parameters')
parser.add_argument('--window-size', type=int, default=28, help='Sliding window size (default: 28)')
parser.add_argument('--transition-window', type=int, default=3, help='Transition window size (default: 3)')
parser.add_argument('--central-metric', type=str, default='robust', choices=['mean', 'median', 'robust'], help='Central metric (default: robust)')
parser.add_argument('--alfa', type=float, default=0.8, help='Uncertainty range fraction (default: 0.8)')
parser.add_argument('--min-delta', type=float, default=0.2, help='Minimum rate change % (default: 0.2)')
parser.add_argument('--max-delta', type=float, default=2, help='Maximum rate change % (default: 2)')
parser.add_argument('--skip-days', type=int, default=5, help='Days to skip after signal (default: 5)')
parser.add_argument('--stability-days', type=int, default=21, help='Stability period days (default: 21)')
parser.add_argument('--stability-fraction', type=float, default=0.5, help='Stability fraction (default: 0.5)')
args = parser.parse_args()

# Load Fed rates and generate signals
df_fed_rates = pd.read_csv("fed_rate_1962_today.csv")

print("🔍 Generating Fed rate signals with parameters:")
print(f"   window_size: {args.window_size}")
print(f"   transition_window: {args.transition_window}")
print(f"   central_metric: {args.central_metric}")
print(f"   alfa: {args.alfa}")
print(f"   min_delta: {args.min_delta}")
print(f"   max_delta: {args.max_delta}")
print(f"   skip_days: {args.skip_days}")
print(f"   stability_days: {args.stability_days}")
print(f"   stability_fraction: {args.stability_fraction}\n")

signals = identify_fed_rate_signals(
    df_fed_rates,
    window_size=args.window_size,
    transition_window=args.transition_window,
    central_metric=args.central_metric,
    alfa=args.alfa,
    min_delta=args.min_delta,
    max_delta=args.max_delta,
    skip_days=args.skip_days,
    stability_days=args.stability_days,
    stability_fraction=args.stability_fraction,
    verbose=False,
)

# === STATIC VERSION (matplotlib) ===
plot_fed_rate_overview(
    df_fed_rates,
    signals)

output_path = "assets/img/fed_signals_overview.png"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"Static graph saved to {output_path}")

# === INTERACTIVE VERSION (plotly) ===
# Prepare data
df = df_fed_rates.copy()
df = df.rename(columns={"Time Period": "Date", "RIFSPFF_N.D": "Fed_rate"})
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date").reset_index(drop=True)

# Create interactive plot
fig = go.Figure()

# Add Fed rate line
fig.add_trace(
    go.Scatter(
        x=df["Date"],
        y=df["Fed_rate"],
        mode='lines',
        name='Fed Rate',
        line=dict(color='steelblue', width=2),
        hovertemplate='<b>Date:</b> %{x|%Y-%m-%d}<br><b>Fed Rate:</b> %{y:.3f}%<extra></extra>'
    )
)

# Add signal markers
for start, end, delta_f in signals:
    start_date = pd.to_datetime(start)
    end_date = pd.to_datetime(end)
    
    # Color based on direction - sharper colors
    color = '#ff0000' if delta_f > 0 else '#00cc00'  # Bright red for increase, bright green for decrease
    
    # Shade the stability period
    fig.add_vrect(
        x0=start_date,
        x1=end_date,
        fillcolor=color,
        opacity=0.15,
        layer="below",
        line_width=0,
    )

# Legend labels for signal direction
fig.add_trace(
    go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='#ff0000', width=6),
        name='Rate increases (red)'
    )
)
fig.add_trace(
    go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='#00cc00', width=6),
        name='Rate decreases (green)'
    )
)

# Update layout
fig.update_layout(
    title='<b>Federal Reserve Interest Rate with Detected Signals</b>',
    xaxis_title='Date',
    yaxis_title='Federal Funds Rate (%)',
    hovermode='x unified',
    template='plotly_white',
    height=600,
    width=1000,
    font=dict(family='Arial, sans-serif', size=12),
    xaxis=dict(
        rangeslider=dict(visible=True),
        type='date'
    )
)

# Save interactive version
interactive_path = "assets/html/fed_signals_interactive.html"
os.makedirs(os.path.dirname(interactive_path), exist_ok=True)
fig.write_html(interactive_path)
print(f"Interactive graph saved to {interactive_path}")

# === CREATE INTERACTIVE HTML WITH SLIDERS ===
html_with_sliders = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }
        .controls {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 6px;
            border: 1px solid #e0e0e0;
        }
        .control-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        label {
            font-weight: bold;
            color: #333;
            font-size: 13px;
        }
        input[type="range"] {
            width: 100%;
            height: 6px;
            cursor: pointer;
        }
        .value-display {
            color: #0066cc;
            font-weight: bold;
            font-size: 14px;
            padding: 4px;
            background: #e6f2ff;
            border-radius: 3px;
            text-align: center;
        }
        button {
            grid-column: span 1;
            padding: 12px 24px;
            background: #0066cc;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.3s;
        }
        button:hover {
            background: #0052a3;
        }
        #graphDiv {
            width: 100%;
            height: 650px;
        }
        .info {
            margin-top: 20px;
            padding: 15px;
            background: #e6f2ff;
            border-left: 4px solid #0066cc;
            border-radius: 4px;
            color: #333;
            font-size: 13px;
            line-height: 1.5;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚙️ Interactive Fed Rate Signal Detector</h1>
        
        <div class="controls">
            <div class="control-group">
                <label for="windowSize">Window Size: <span class="value-display" id="windowSizeValue">28</span></label>
                <input type="range" id="windowSize" min="14" max="60" value="28" step="1">
            </div>
            
            <div class="control-group">
                <label for="transitionWindow">Transition Window: <span class="value-display" id="transitionWindowValue">3</span></label>
                <input type="range" id="transitionWindow" min="1" max="7" value="3" step="1">
            </div>
            
            <div class="control-group">
                <label for="alfa">Alfa (Uncertainty): <span class="value-display" id="alfaValue">0.80</span></label>
                <input type="range" id="alfa" min="0.2" max="1.5" value="0.8" step="0.1">
            </div>
            
            <div class="control-group">
                <label for="minDelta">Min Delta (%): <span class="value-display" id="minDeltaValue">0.20</span></label>
                <input type="range" id="minDelta" min="0.1" max="1.0" value="0.2" step="0.1">
            </div>
            
            <div class="control-group">
                <label for="maxDelta">Max Delta (%): <span class="value-display" id="maxDeltaValue">2.00</span></label>
                <input type="range" id="maxDelta" min="1" max="4" value="2" step="0.1">
            </div>
            
            <div class="control-group">
                <label for="skipDays">Skip Days: <span class="value-display" id="skipDaysValue">5</span></label>
                <input type="range" id="skipDays" min="1" max="15" value="5" step="1">
            </div>
            
            <div class="control-group">
                <label for="stabilityDays">Stability Days: <span class="value-display" id="stabilityDaysValue">21</span></label>
                <input type="range" id="stabilityDays" min="7" max="60" value="21" step="1">
            </div>
            
            <div class="control-group">
                <label for="stabilityFraction">Stability Fraction: <span class="value-display" id="stabilityFractionValue">0.50</span></label>
                <input type="range" id="stabilityFraction" min="0.1" max="1.0" value="0.5" step="0.1">
            </div>
            
            <button onclick="generateGraph()">🔄 Update Graph</button>
        </div>
        
        <div id="graphDiv"></div>
        
        <div class="info">
            <strong>How to use:</strong> Adjust the sliders to change signal detection parameters, then click "Update Graph" to see how the signals change.
            The red shaded areas represent rate increase periods, and green areas represent rate decrease periods.
        </div>
    </div>

    <script>
        // Update value displays when sliders change
        const sliders = document.querySelectorAll('input[type="range"]');
        sliders.forEach(slider => {
            slider.addEventListener('input', function() {
                const valueName = this.id + 'Value';
                const valueEl = document.getElementById(valueName);
                if (valueEl) {
                    const val = parseFloat(this.value);
                    valueEl.textContent = val.toFixed(2);
                }
            });
        });

        async function generateGraph() {
            // Get current parameter values
            const params = {
                window_size: parseInt(document.getElementById('windowSize').value),
                transition_window: parseInt(document.getElementById('transitionWindow').value),
                alfa: parseFloat(document.getElementById('alfa').value),
                min_delta: parseFloat(document.getElementById('minDelta').value),
                max_delta: parseFloat(document.getElementById('maxDelta').value),
                skip_days: parseInt(document.getElementById('skipDays').value),
                stability_days: parseInt(document.getElementById('stabilityDays').value),
                stability_fraction: parseFloat(document.getElementById('stabilityFraction').value)
            };

            console.log('Generating graph with parameters:', params);
            
            // In a real implementation, this would call a backend API
            // For now, show a message
            alert('🔄 Please run the Python script with custom parameters:\\n\\npython generate_alexis_graphs.py \\\\\\n  --window-size ' + params.window_size + ' \\\\\\n  --transition-window ' + params.transition_window + ' \\\\\\n  --alfa ' + params.alfa + ' \\\\\\n  --min-delta ' + params.min_delta + ' \\\\\\n  --max-delta ' + params.max_delta + ' \\\\\\n  --skip-days ' + params.skip_days + ' \\\\\\n  --stability-days ' + params.stability_days + ' \\\\\\n  --stability-fraction ' + params.stability_fraction);
        }

        // Load the initial graph
        window.onload = function() {
            fetch('fed_signals_interactive.html')
                .then(response => response.text())
                .then(html => {
                    // Extract plotly data from the html file
                    // For now, just show the current graph
                });
        };
    </script>
</body>
</html>
"""

sliders_path = "assets/html/fed_signals_interactive_sliders.html"
os.makedirs(os.path.dirname(sliders_path), exist_ok=True)
with open(sliders_path, 'w', encoding='utf-8') as f:
    f.write(html_with_sliders)
print(f"Interactive sliders page saved to {sliders_path}")

print("✅ Both graphs generated successfully!")
