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

<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>




<script>
 
function renderMplExport(divId, jsonPath) {
  fetch(jsonPath)
    .then(r => r.json())
    .then(d => {

      /* =======================
         DATAFRAME EXPORTS
         ======================= */

      // line (multi-line)
      if (d.type === "dataframe" && d.kind === "line") {
        const traces = (d.series || []).map(s => ({
          x: d.x, y: s.y, name: s.name,
          type: "scatter", mode: "lines"
        }));
        Plotly.newPlot(divId, traces, {
          title: d.title || "",
          xaxis: { title: d.xlabel || "" },
          yaxis: { title: d.ylabel || "" }
        }, { responsive: true });
        return;
      }

      // stacked area
      if (d.type === "dataframe" && d.kind === "stacked") {
        const traces = (d.series || []).map(s => ({
          x: d.x, y: s.y, name: s.name,
          type: "scatter", mode: "lines", stackgroup: "one"
        }));
        Plotly.newPlot(divId, traces, {
          title: d.title || "",
          xaxis: { title: d.xlabel || "" },
          yaxis: { title: d.ylabel || "" }
        }, { responsive: true });
        return;
      }

      // horizontal bars with zero line (fig09/fig11 style)
      if (d.type === "dataframe" && d.kind === "barh_zero") {
        Plotly.newPlot(divId, [{
          x: d.values, y: d.categories,
          type: "bar", orientation: "h"
        }], {
          title: d.title || "",
          xaxis: { title: d.xlabel || "", zeroline: false },
          yaxis: { automargin: true },
          shapes: [{
            type: "line",
            x0: d.zero_line ?? 0, x1: d.zero_line ?? 0,
            y0: -0.5, y1: d.categories.length - 0.5,
            line: { color: "black", width: 1, dash: "dash" }
          }]
        }, { responsive: true });
        return;
      }

      // line + horizontal thresholds (fig08 style)
      if (d.type === "dataframe" && d.kind === "line_thresholds") {
        const traces = [{
          x: d.x,
          y: d.series?.[0]?.y || [],
          name: d.series?.[0]?.name || "Series",
          type: "scatter",
          mode: "lines",
          line: { width: 2 }
        }];

        const x0 = d.x?.[0];
        const x1 = d.x?.[d.x.length - 1];

        (d.thresholds || []).forEach((t, i) => {
          const y = (typeof t === "number") ? t : t.y;
          const name = (typeof t === "number") ? (d.threshold_labels?.[i] || `Threshold ${i+1}`) : (t.label || `Threshold ${i+1}`);
          const color = (typeof t === "number") ? undefined : (t.color || undefined);

          traces.push({
            x: [x0, x1],
            y: [y, y],
            type: "scatter",
            mode: "lines",
            name,
            line: { dash: "dash", width: 2, color }
          });
        });

        Plotly.newPlot(divId, traces, {
          title: d.title || "",
          xaxis: { title: d.xlabel || "" },
          yaxis: { title: d.ylabel || "" }
        }, { responsive: true });
        return;
      }


        // horizontal error bars with zero line (fig03 style)
        if (d.type === "dataframe" && d.kind === "errorbar_h_zero") {
          const n = (d.categories || []).length;
        
          Plotly.newPlot(divId, [{
            x: d.x,
            y: d.categories,
            type: "scatter",
            mode: "markers",
            error_x: {
              type: "data",
              symmetric: true,
              array: d.xerr   // ✅ single symmetric CI array
            }
          }], {
            title: d.title || "",
            xaxis: { title: d.xlabel || "", zeroline: false },
            yaxis: { automargin: true },
            shapes: [{
              type: "line",
              x0: d.zero_line ?? 0,
              x1: d.zero_line ?? 0,
              y0: -0.5,
              y1: n - 0.5,
              line: { color: "black", width: 1, dash: "dash" }
            }]
          }, { responsive: true });
        
          return;
        }


        // dual horizontal error bars with y-offset + zero line (fig03 style)
        if (d.type === "dataframe" && d.kind === "errorbar_h_dual") {
          const n = (d.categories || []).length;
          const yBase = Array.from({ length: n }, (_, i) => i);
          const offsets = d.y_offsets || [-0.15, +0.15];
        
          const traces = (d.series || []).map((s, i) => ({
            x: s.x,
            y: yBase.map(v => v + (offsets[i] ?? 0)),
            type: "scatter",
            mode: "markers",
            name: s.name,
            error_x: { type: "data", symmetric: true, array: s.xerr }
          }));
        
          Plotly.newPlot(divId, traces, {
            title: d.title || "",
            xaxis: { title: d.xlabel || "", zeroline: false },
            yaxis: {
              tickmode: "array",
              tickvals: yBase,
              ticktext: d.categories,
              automargin: true
            },
            shapes: [{
              type: "line",
              x0: d.zero_line ?? 0, x1: d.zero_line ?? 0,
              y0: -0.5, y1: n - 0.5,
              line: { color: "black", width: 1, dash: "dash" }
            }]
          }, { responsive: true });
        
          return;
        }

                
        // boxplot from raw grouped values (fig04 style)
        if (d.type === "dataframe" && d.kind === "box_raw") {
          const traces = (d.groups || []).map(g => ({
            type: "box",
            name: g.name,
            y: g.y,
            boxpoints: "outliers"   // shows the circles like seaborn
          }));
        
          Plotly.newPlot(divId, traces, {
            title: d.title || "",
            xaxis: { title: d.xlabel || "" },
            yaxis: { title: d.ylabel || "" }
          }, { responsive: true });
        
          return;
        }

        
        // scatter with text labels + zero lines (fig07 style)
        if (d.type === "dataframe" && d.kind === "scatter_labels_zero") {
          const trace = {
            x: d.x,
            y: d.y,
            type: "scatter",
            mode: "markers+text",
            text: d.labels,
            textposition: "top center",
            marker: { size: 10 },
            hovertemplate: "%{text}<br>x=%{x:.4f}<br>y=%{y:.4f}<extra></extra>"
          };
        
          Plotly.newPlot(divId, [trace], {
            title: d.title || "",
            xaxis: { title: d.xlabel || "" },
            yaxis: { title: d.ylabel || "" },
            shapes: [
              { // vertical x=0
                type: "line",
                x0: d.zero_x ?? 0, x1: d.zero_x ?? 0,
                y0: Math.min(...d.y), y1: Math.max(...d.y),
                line: { color: "black", width: 1 }
              },
              { // horizontal y=0
                type: "line",
                x0: Math.min(...d.x), x1: Math.max(...d.x),
                y0: d.zero_y ?? 0, y1: d.zero_y ?? 0,
                line: { color: "black", width: 1 }
              }
            ]
          }, { responsive: true });
        
          return;
        }


        // horizontal bars with hover p-values + zero line (fig09 style)
        if (d.type === "dataframe" && d.kind === "barh_hover_pvalue") {
        
          const traces = [{
            x: d.values,
            y: d.categories,
            type: "bar",
            orientation: "h",
              
            text: (d.p_values || []).map(p => {
              if (p === null || p === undefined) return "";
              const pn = Number(p);
              if (!isFinite(pn)) return "";
              return "p = " + pn.toExponential(2);
            }),

              
            hovertemplate:
              "<b>%{y}</b><br>" +
              "Δ return: %{x:.2f}%<br>" +
              "%{text}<extra></extra>"
          }];
        
          Plotly.newPlot(divId, traces, {
            title: d.title || "",
            xaxis: {
              title: d.xlabel || "",
              zeroline: false
            },
            yaxis: {
              automargin: true
            },
            shapes: [{
              type: "line",
              x0: d.zero_line ?? 0,
              x1: d.zero_line ?? 0,
              y0: -0.5,
              y1: d.categories.length - 0.5,
              line: { color: "black", width: 1 }
            }]
          }, { responsive: true });
        
          return;
        }
                    
                
        // horizontal error bars (asymmetric) with dashed zero line (fig12 style)
        if (d.type === "dataframe" && d.kind === "errorbar_h_zero_asym") {
          const n = (d.categories || []).length;
        
          Plotly.newPlot(divId, [{
            x: d.x,
            y: d.categories,
            type: "scatter",
            mode: "markers",
            error_x: {
              type: "data",
              symmetric: false,
              array: (d.xerr_high || []).map(Number),
              arrayminus: (d.xerr_low || []).map(Number)
            }
          }], {
            title: d.title || "",
            xaxis: { title: d.xlabel || "", zeroline: false },
            yaxis: { automargin: true },
            shapes: [{
              type: "line",
              x0: d.zero_line ?? 0,
              x1: d.zero_line ?? 0,
              y0: -0.5,
              y1: n - 0.5,
              line: { color: "black", width: 1, dash: "dash" }   // dashed like matplotlib
            }]
          }, { responsive: true });
        
          return;
        }


        // scatter with categorical y + p-value annotations + vertical zero line (fig18 style)
        if (d.type === "dataframe" && d.kind === "scatter_labels_zero_p") {
          const x = (d.x || []).map(Number);
          const cats = d.categories || [];
          const p = d.p_values || [];
        
          const trace = {
            x: x,
            y: cats,
            type: "scatter",
            mode: "markers+text",
            text: p.map(v => {
              const pn = Number(v);
              if (!isFinite(pn)) return "";
              return "p=" + pn.toPrecision(3);
            }),
            textposition: "middle right",
            marker: { size: 10 },
            hovertemplate: "<b>%{y}</b><br>x=%{x:.4f}<extra></extra>"
          };
        
          // span the categorical axis safely
          const y0 = -0.5;
          const y1 = cats.length - 0.5;
        
          Plotly.newPlot(divId, [trace], {
            title: d.title || "",
            xaxis: { title: d.xlabel || "", zeroline: false },
            yaxis: { automargin: true, type: "category" },
            shapes: [{
              type: "line",
              x0: d.zero_x ?? 0, x1: d.zero_x ?? 0,
              y0: y0, y1: y1,
              xref: "x",
              yref: "y",
              line: { color: "black", width: 1, dash: "dash" }
            }]
          }, { responsive: true });
        
          return;
        }

        
        // dumbbell: naive vs controlled (fig20 style)
        if (d.type === "dataframe" && d.kind === "dumbbell_naive_controlled") {
          const cats = d.categories || [];
          const x1 = (d.x_naive || []).map(Number);
          const x2 = (d.x_ctrl || []).map(Number);
        
          // segments (one trace with gaps)
          const segX = [];
          const segY = [];
          for (let i = 0; i < cats.length; i++) {
            segX.push(x1[i], x2[i], null);
            segY.push(cats[i], cats[i], null);
          }
        
          const traces = [
            {
              x: segX, y: segY,
              type: "scatter", mode: "lines",
              name: "",
              hoverinfo: "skip",
              line: { width: 1 },
              showlegend: false
            },
            {
              x: x1, y: cats,
              type: "scatter", mode: "markers",
              name: d.name_naive || "Naive",
              hovertemplate: "<b>%{y}</b><br>Naive: %{x:.3f}<extra></extra>"
            },
            {
              x: x2, y: cats,
              type: "scatter", mode: "markers",
              name: d.name_ctrl || "Controlled",
              hovertemplate: "<b>%{y}</b><br>Controlled: %{x:.3f}<extra></extra>"
            }
          ];
        
        Plotly.newPlot(divId, traces, {
          title: d.title || "",
          xaxis: { title: d.xlabel || "" },
          yaxis: { automargin: true },
        
          legend: {
            orientation: "h",
            x: 0.5,
            xanchor: "center",
            y: -0.25   // ⬅ pushes legend below plot
          },
        
          margin: {
            l: 120,
            r: 40,
            t: 60,
            b: 120     // ⬅ reserve space so legend never overlaps
          }
        }, { responsive: true });

          return;
        }
            
       
        
        // stacked horizontal bars + star annotations (fig22 style)
        if (d.type === "dataframe" && d.kind === "barh_stacked_star") {
          const cats = d.categories || [];
          const macro = (d.macro || []).map(Number);
          const fed = (d.fed_inc || []).map(Number);
          const star = d.star || [];
        
          const t1 = {
            x: macro, y: cats,
            type: "bar", orientation: "h",
            name: d.labels?.macro || "Macro risk + volatility persistence",
            hovertemplate: "<b>%{y}</b><br>Macro: %{x:.3f}<extra></extra>"
          };
        
          const t2 = {
            x: fed, y: cats,
            type: "bar", orientation: "h",
            name: d.labels?.fed_inc || "Incremental Fed contribution (given macro)",
            hovertemplate: "<b>%{y}</b><br>Fed inc: %{x:.3f}<extra></extra>"
          };
        
          // star annotations
          const ann = [];
          for (let i = 0; i < cats.length; i++) {
            if (star[i]) {
              const tot = (macro[i] || 0) + (fed[i] || 0);
              ann.push({
                x: tot + 0.01,
                y: cats[i],
                xref: "x",
                yref: "y",
                text: "*",
                showarrow: false,
                font: { size: 18 },
                xanchor: "left"
              });
            }
          }
        
          Plotly.newPlot(divId, [t1, t2], {
            title: d.title || "",
            barmode: "stack",
            xaxis: { title: d.xlabel || "", zeroline: false, showgrid: true },
            yaxis: { automargin: true, type: "category", autorange: "reversed" },
            annotations: ann,
        
            // legend below + extra space
            legend: { orientation: "h", x: 0.5, xanchor: "center", y: -0.35 },
            margin: { t: 70, b: 170, l: 140, r: 60 },
            height: 650
          }, { responsive: true });
        
          return;
        }

                    

        
      /* =======================
         MATPLOTLIB EXPORTS
         ======================= */
      if (d.type === "matplotlib_export") {
        const traces = [];
        const shapes = [];

        (d.axes || []).forEach((ax, axIndex) => {
          // lines
          (ax.lines || []).forEach(l => traces.push({
            x: l.x, y: l.y,
            type: "scatter", mode: "lines",
            name: (l.label && !l.label.startsWith("_")) ? l.label : ""
          }));

          // scatters
          (ax.scatters || []).forEach(s => traces.push({
            x: s.x, y: s.y,
            type: "scatter", mode: "markers",
            name: (s.label && !s.label.startsWith("_")) ? s.label : ""
          }));

          // polygons (areas)
          (ax.polygons || []).forEach(pg => (pg.polys || []).forEach(p => traces.push({
            x: p.x, y: p.y,
            type: "scatter", mode: "lines",
            fill: "toself",
            name: (pg.label && !pg.label.startsWith("_")) ? pg.label : ""
          })));

          // bars (rectangles)
          (ax.bars || []).forEach(b => {
            // If it's actually a bar chart exported as rectangles, plot as bar at center
            traces.push({
              x: [b.x + b.width / 2],
              y: [b.height],
              type: "bar",
              name: ""
            });
          });

          // optional: vertical/horizontal guide lines (if you exported them as shapes)
          // If you later export "hline"/"vline" explicitly, we can support it here.
        });

        Plotly.newPlot(divId, traces, {
          title: d.axes?.[0]?.title || "",
          xaxis: { title: d.axes?.[0]?.xlabel || "" },
          yaxis: { title: d.axes?.[0]?.ylabel || "" },
          shapes
        }, { responsive: true });
        return;
      }

      // Fallback: show what it is instead of breaking the page
      Plotly.newPlot(divId, [], {
        title: "Unsupported JSON",
        annotations: [{ text: `type=${d.type}, kind=${d.kind}`, showarrow: false }]
      }, { responsive: true });

    })
    .catch(err => {
      Plotly.newPlot(divId, [], {
        title: "JSON load error",
        annotations: [{ text: String(err), showarrow: false }]
      }, { responsive: true });
    });
}


function renderSectorPickerDualAxis(divId, jsonPath, selectId) {
  fetch(jsonPath).then(r => r.json()).then(d => {
    const sel = document.getElementById(selectId);
    sel.innerHTML = "";
    (d.sectors || []).forEach(s => {
      const opt = document.createElement("option");
      opt.value = s; opt.textContent = s;
      sel.appendChild(opt);
    });

    function draw(sector) {
      const trFed = { x: d.x, y: d.fed.y, type:"scatter", mode:"lines", name:d.fed.name, yaxis:"y1" };
      const trVol = { x: d.x, y: d.vol.by_sector[sector], type:"scatter", mode:"lines", name:d.vol.name, yaxis:"y2" };

      Plotly.newPlot(divId, [trFed, trVol], {
        title: d.title || "",
        xaxis: { title: d.xlabel || "" },
        yaxis: { title: "ΔFedRate", range: d.fed.ylim, zeroline: true },
        yaxis2: { title: "Volatility", range: d.vol.ylim, overlaying: "y", side: "right", zeroline: true },
        legend: { orientation: "h" }
      }, { responsive: true });
    }

    sel.onchange = () => draw(sel.value);
    sel.value = d.sectors?.[0] || "";
    draw(sel.value);
  });
}
renderSectorPickerDualAxis("fig19", "{{ site.baseurl }}/assets/fig_json/fig19.json", "fig19_sector");
    
</script>






<div class="top-nav">
    <div class="top-nav-content">
        <a href="{{ site.baseurl }}/" class="nav-link">Home</a>
        <a href="{{ site.baseurl }}/other_page" class="nav-link">Analysis</a>
        <a href="{{ site.baseurl }}/game" class="nav-link">Interactive</a>
        <a href="{{ site.baseurl }}/Beatrice" class="nav-link active">Beatrice</a>
        <a href="{{ site.baseurl }}/Cyriac" class="nav-link">Cyriac</a>
        <a href="{{ site.baseurl }}/Lucas" class="nav-link">Lucas</a>
        <a href="{{ site.baseurl }}/Alexis" class="nav-link">Alexis</a>
        <a href="{{ site.github.repository_url }}" class="nav-link" target="_blank">Repository</a>
    </div>
</div>

BEATRICE AAAAAAAAAAAAAAAAAAAAAAAAA


# Hello, this is my page
I am trying stuff to see how it works.

Paragraph 1
P2

List
- item 1
- item 2

**bold**




Text can be **bold**, _italic_, or ~~strikethrough~~.

[Link to another page](./another-page.html).

There should be whitespace between paragraphs.

There should be whitespace between paragraphs. We recommend including a README, or a file with information about your project.

<div id="fig01" style="width:100%; height:520px;"></div>
<script>renderMplExport("fig01", "{{ site.baseurl }}/assets/fig_json/fig01.json");</script>

<div id="fig02" style="width:100%; height:520px;"></div>
<script>renderMplExport("fig02", "{{ site.baseurl }}/assets/fig_json/fig02.json");</script>

<div id="fig03" style="width:100%; height:520px;"></div>
<script>renderMplExport("fig03", "{{ site.baseurl }}/assets/fig_json/fig03.json");</script>

<div id="fig04" style="width:100%; height:520px;"></div>
<script>renderMplExport("fig04", "{{ site.baseurl }}/assets/fig_json/fig04.json");</script>

<div id="fig05" style="width:100%; height:520px;"></div>
<script>renderMplExport("fig05", "{{ site.baseurl }}/assets/fig_json/fig05.json");</script>

<div id="fig06" style="width:100%; height:520px;"></div>
<script>renderMplExport("fig06", "{{ site.baseurl }}/assets/fig_json/fig06.json");</script>

<div id="fig07" style="width:100%; height:520px;"></div>
<script>renderMplExport("fig07", "{{ site.baseurl }}/assets/fig_json/fig07.json");</script>

<div id="fig08" style="width:100%; height:520px;"></div>
<script>renderMplExport("fig08", "{{ site.baseurl }}/assets/fig_json/fig08.json");</script>

<div id="fig09" style="width:100%; height:520px;"></div>
<script>renderMplExport("fig09", "{{ site.baseurl }}/assets/fig_json/fig09.json");</script>

<div id="fig11" style="width:100%; height:520px;"></div>
<script>renderMplExport("fig11", "{{ site.baseurl }}/assets/fig_json/fig11.json");</script>

<div id="fig12" style="width:100%; height:520px;"></div>
<script>
  renderMplExport("fig12", "{{ site.baseurl }}/assets/fig_json/fig12.json");
</script>

<!--

<div id="fig13" style="width:100%; height:520px;"></div>
<script>renderMplExport("fig13", "{{ site.baseurl }}/assets/fig_json/fig13.json");</script>

<div id="fig14" style="width:100%; height:520px;"></div>
<script>renderMplExport("fig14", "{{ site.baseurl }}/assets/fig_json/fig14.json");</script>

<div id="fig15" style="width:100%; height:520px;"></div>
<script>renderMplExport("fig15", "{{ site.baseurl }}/assets/fig_json/fig15.json");</script>

<div id="fig16" style="width:100%; height:520px;"></div>
<script>renderMplExport("fig16", "{{ site.baseurl }}/assets/fig_json/fig16.json");</script>

-->

<div id="fig17" style="width:100%; height:520px;"></div>
<script>renderMplExport("fig17", "{{ site.baseurl }}/assets/fig_json/fig17.json");</script>

<div id="fig18" style="width:100%; height:520px;"></div>
<script>renderMplExport("fig18", "{{ site.baseurl }}/assets/fig_json/fig18.json");</script>

<div style="margin:10px 0;">
  <label for="fig19_sector"><b>Sector:</b></label>
  <select id="fig19_sector"></select>
</div>

<div id="fig19" style="width:100%; height:520px;"></div>

<script>
  renderSectorPickerDualAxis(
    "fig19",
    "{{ site.baseurl }}/assets/fig_json/fig19.json",
    "fig19_sector"
  );
</script>

<div id="fig20" style="width:100%; height:560px;"></div>
<script>renderMplExport("fig20", "{{ site.baseurl }}/assets/fig_json/fig20.json");</script>

<div id="fig21" style="width:100%; height:520px;"></div>
<script>
  renderMplExport("fig21", "{{ site.baseurl }}/assets/fig_json/fig21.json");
</script>

<div id="fig22" style="width:100%; height:700px;"></div>
<script>
  renderMplExport("fig22", "{{ site.baseurl }}/assets/fig_json/fig22.json");
</script>


TEST

<!-- ===================== -->
<!-- PART 1 -->
<!-- ===================== -->

<section class="sector-part" id="part-1">

<h2>1. Why sector-level analysis? Market vs sector behavior over time</h2>

<p class="interviewer">
<b>Interviewer:</b> Why do we need sector-level analysis rather than just looking at the market as a whole?
</p>

<h3>Context</h3>
<p>
Equity markets are often summarized by a single index, implicitly assuming that firms respond
homogeneously to macroeconomic forces. In reality, sectors differ fundamentally in their
production structure, capital intensity, exposure to interest rates, and dependence on future
growth expectations.
</p>
<p>
From a valuation perspective, equity prices reflect discounted future cash flows. If sectors
differ in the timing and riskiness of these cash flows, then even under identical market
conditions, their performance can diverge substantially. Monetary policy, technological change,
and structural economic shifts can therefore generate persistent sectoral dispersion rather than
short-lived noise.
</p>
<p>
Before studying monetary policy effects, it is essential to establish a baseline: how much of
sector performance is driven by the overall market, and how much reflects sector-specific
dynamics?
</p>

<h3>Method</h3>
<p>
For each sector <em>s</em>, we compute log-returns:
</p>
<p class="math">
r<sub>s,t</sub> = ln(P<sub>s,t</sub> / P<sub>s,t−1</sub>)
</p>
<p>
Returns are aggregated into cumulative returns rebased to 1:
</p>
<p class="math">
CR<sub>s,t</sub> = ∏<sub>τ≤t</sub> (1 + r<sub>s,τ</sub>)
</p>
<p>
To isolate sector-specific behavior, we estimate a CAPM-style market model:
</p>
<p class="math">
r<sub>s,t</sub> = α<sub>s</sub> + β<sub>s</sub> r<sub>m,t</sub> + ε<sub>s,t</sub>
</p>
<p>
where β<sub>s</sub> measures exposure to systematic market risk and α<sub>s</sub> captures
average excess performance unexplained by the market.
</p>

<h3>Results</h3>

<div class="figure-block">
  <!-- FIG 1 -->
</div>

<div class="figure-block">
  <!-- FIG 4 -->
</div>

<div class="figure-block">
  <!-- FIG 5 -->
</div>

<p>
Cumulative returns reveal large and persistent divergence across sectors. While all sectors benefit
from long-run market growth, the magnitude differs dramatically. Some sectors strongly outperform
the market over decades, while others lag persistently. These deviations are not transitory and
widen during major macroeconomic episodes.
</p>

<h3>Conclusion</h3>
<p>
Market exposure explains a large fraction of sector returns, but not their relative trajectories.
This motivates studying additional drivers—starting with monetary policy—that may shape
sector-specific outcomes beyond the market factor.
</p>

</section>

<!-- ===================== -->
<!-- PART 2 -->
<!-- ===================== -->

<section class="sector-part" id="part-2">

<h2>2. How sensitive are different sectors to changes in the Fed rate?</h2>

<p class="interviewer">
<b>Interviewer:</b> Are all sectors equally sensitive to changes in the Fed policy rate?
</p>

<h3>Context</h3>
<p>
Changes in the Fed policy rate affect borrowing costs, discount rates, liquidity conditions, and
risk appetite. However, these channels do not operate uniformly across sectors. Sectors differ in
their reliance on external financing, growth expectations, and balance-sheet structure.
</p>
<p>
Measuring sector-level sensitivity allows us to test whether monetary policy transmission is
homogeneous or sector-specific.
</p>

<h3>Method</h3>
<p>
We estimate sector-specific regressions controlling for market movements:
</p>
<p class="math">
r<sub>s,t</sub> = α<sub>s</sub> + β<sub>s</sub> r<sub>m,t</sub> + γ<sub>s</sub> ΔFedRate<sub>t</sub> + u<sub>s,t</sub>
</p>
<p>
The coefficient γ<sub>s</sub> measures the marginal sensitivity of sector returns to changes
in the policy rate, conditional on the market. Robust standard errors are used.
</p>

<h3>Results</h3>

<div class="figure-block">
  <!-- FIG 7 -->
</div>

<p>
Market exposure and Fed sensitivity emerge as distinct dimensions of risk. Some sectors exhibit
meaningful sensitivity to policy rate changes, while others are weakly affected despite similar
market exposure.
</p>

<h3>Conclusion</h3>
<p>
Fed rate changes matter for sector returns, but heterogeneously. Monetary policy adds an
independent source of sector-level risk beyond the market factor.
</p>

</section>

<!-- ===================== -->
<!-- PART 3 -->
<!-- ===================== -->

<section class="sector-part" id="part-3">

<h2>3. How do sectors react to sudden Fed signals and surprise cuts?</h2>

<p class="interviewer">
<b>Interviewer:</b> Do sectors react differently when the Fed moves unexpectedly?
</p>

<h3>Context</h3>
<p>
Not all policy actions convey the same information. Surprise rate cuts reveal new information about
economic conditions or financial stress. Markets may react to the signal embedded in the policy
decision rather than to the mechanical effect of lower rates.
</p>

<h3>Method</h3>
<p>
We implement a short-horizon event-study framework around surprise Fed cuts. Sector performance is
measured relative to a benchmark sector (Industrials):
</p>
<p class="math">
AR<sub>s,t</sub> = r<sub>s,t</sub> − r<sub>Ind,t</sub>
</p>
<p>
Abnormal returns are aggregated over a 3-day window to obtain cumulative abnormal returns.
</p>

<h3>Results</h3>

<div class="figure-block">
  <!-- FIG 11 -->
</div>

<div class="figure-block">
  <!-- FIG 12 -->
</div>

<p>
Sector responses to surprise cuts are highly heterogeneous. Some sectors underperform sharply,
suggesting that surprise easing is often interpreted as bad news about the macroeconomic outlook.
</p>

<h3>Conclusion</h3>
<p>
Short-term responses to surprise Fed actions depend critically on sector characteristics and the
informational content of policy decisions.
</p>

</section>

<!-- ===================== -->
<!-- PART 4 -->
<!-- ===================== -->

<section class="sector-part" id="part-4">

<h2>4. Are Fed rates the right proxy for long-term monetary policy?</h2>

<p class="interviewer">
<b>Interviewer:</b> Is the Fed policy rate the best variable to study long-term stock market effects?
</p>

<h3>Context</h3>
<p>
Equity valuation depends on discounting future cash flows over long horizons. While the Fed Funds
Rate governs short-term conditions, long-term yields incorporate expectations about future policy,
inflation, and risk premia.
</p>

<h3>Method</h3>
<p>
We compare the dynamics of the Fed Funds Rate and the 10-year Treasury yield, and use the latter as
a proxy for long-term monetary conditions.
</p>

<h3>Results</h3>

<div class="figure-block">
  <!-- FIG 2 -->
</div>

<p>
The two rates co-move closely, but the 10-year yield is smoother and forward-looking, making it
more suitable for long-horizon sector analysis.
</p>

<h3>Conclusion</h3>
<p>
The Fed rate captures short-term policy actions, while the 10Y yield better reflects long-term
monetary conditions relevant for equity valuation.
</p>

</section>

<!-- ===================== -->
<!-- PART 5 -->
<!-- ===================== -->

<section class="sector-part" id="part-5">

<h2>5. Which sectors perform better in high-rate environments?</h2>

<p class="interviewer">
<b>Interviewer:</b> Which sectors benefit—or suffer—when long-term interest rates are high?
</p>

<h3>Context</h3>
<p>
High-rate environments alter discounting and macroeconomic conditions. Sector performance depends
on cash-flow timing, pricing power, and balance-sheet exposure.
</p>

<h3>Method</h3>
<p>
We estimate sector sensitivity to changes in the 10Y yield:
</p>
<p class="math">
r<sub>s,t</sub> = α<sub>s</sub> + β<sub>s</sub> r<sub>m,t</sub> + θ<sub>s</sub> ΔY<sub>t</sub><sup>10</sup> + u<sub>s,t</sub>
</p>
<p>
We also define low- and high-rate regimes using yield quantiles and compare average annualized
sector returns across regimes.
</p>

<h3>Results</h3>

<div class="figure-block">
  <!-- FIG 3 -->
</div>

<div class="figure-block">
  <!-- FIG 8 -->
</div>

<div class="figure-block">
  <!-- FIG 9 -->
</div>

<p>
Sector performance differs sharply across rate regimes. Some sectors outperform significantly in
high-rate environments, while others underperform, with statistically meaningful differences.
</p>

<h3>Conclusion</h3>
<p>
High interest rates do not uniformly depress equities. Instead, they redistribute performance
across sectors, confirming the importance of sector-level analysis for understanding monetary
policy effects.
</p>

</section>
TEST





# Header 1

This is a normal paragraph following a header. GitHub is a code hosting platform for version control and collaboration. It lets you and others work together on projects from anywhere.

## Header 2

> This is a blockquote following a header.
>
> When something is important enough, you do it even if the odds are not in your favor.

### Header 3

```js
// Javascript code with syntax highlighting.
var fun = function lang(l) {
  dateformat.i18n = require('./lang/' + l)
  return true;
}
```
