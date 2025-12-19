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

<!--

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

HERE

<div id="fig13" style="width:100%; height:520px;"></div>
<script>renderMplExport("fig13", "{{ site.baseurl }}/assets/fig_json/fig13.json");</script>

<div id="fig14" style="width:100%; height:520px;"></div>
<script>renderMplExport("fig14", "{{ site.baseurl }}/assets/fig_json/fig14.json");</script>

<div id="fig15" style="width:100%; height:520px;"></div>
<script>renderMplExport("fig15", "{{ site.baseurl }}/assets/fig_json/fig15.json");</script>

<div id="fig16" style="width:100%; height:520px;"></div>
<script>renderMplExport("fig16", "{{ site.baseurl }}/assets/fig_json/fig16.json");</script>

HERE

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

-->




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

For each sector s, we compute log-returns:

<blockquote style="margin:16px 0;padding:12px 16px;border-left:4px solid #cbd5e1;background:#f8fafc;">
  <img src="https://latex.codecogs.com/png.image?\dpi{150}r_{s,t}=\ln\!\left(\frac{P_{s,t}}{P_{s,t-1}}\right)" height="60em">
  <p style="margin:10px 0 0;font-style:italic;">
    With rₛ,ₜ the log-return of sector <b>s</b> at time <b>t</b>.
  </p>
</blockquote>


Returns are aggregated into cumulative returns rebased to 1:
<blockquote style="margin:16px 0;padding:12px 16px;border-left:4px solid #cbd5e1;background:#f8fafc;">
  <img src="https://latex.codecogs.com/png.image?\dpi{150}CR_{s,t}=\prod_{\tau\le t}(1+r_{s,\tau})" height="70em">
  <p style="margin:10px 0 0;font-style:italic;">
    Cumulative return rebased to 1, obtained by compounding sector returns over time.
  </p>
</blockquote>



<p>
To isolate sector-specific behavior, we estimate a CAPM-style market model:
</p>

<blockquote style="margin:16px 0;padding:12px 16px;border-left:4px solid #cbd5e1;background:#f8fafc;">
  <img src="https://latex.codecogs.com/png.image?\dpi{150}r_{s,t}=\alpha_s+\beta_s r_{m,t}+\varepsilon_{s,t}" height="70em">
  <p style="margin:10px 0 0;font-style:italic;">
    βₛ measures exposure to market risk, while αₛ captures average excess performance.
  </p>
</blockquote>


<h3>Results</h3>

<div class="figure-block">
  <div id="fig01" style="width:100%; height:520px;"></div>
  <script>renderMplExport("fig01", "{{ site.baseurl }}/assets/fig_json/fig01.json");</script>
</div>

<div style="margin:20px 0;padding:16px;background:#f0f9ff;border-left:4px solid #0ea5e9;border-radius:4px;">
  <h4 style="margin:0 0 8px;color:#0369a1;">💡 How to Read This Chart:</h4>
  <ul style="margin:0;padding-left:20px;color:#1e293b;">
    <li><strong>Higher curves:</strong> sectors that grew more over the period (stronger cumulative performance).</li>
    <li><strong>Diverging curves:</strong> increasing dispersion across sectors (winners vs laggards).</li>
    <li><strong>Sharp bends:</strong> periods of major market stress or regime changes affecting sectors differently.</li>
  </ul>
</div>



<div class="figure-block">
  <div id="fig04" style="width:100%; height:520px;"></div>
  <script>renderMplExport("fig04", "{{ site.baseurl }}/assets/fig_json/fig04.json");</script>
</div>

<div style="margin:20px 0;padding:16px;background:#f0f9ff;border-left:4px solid #0ea5e9;border-radius:4px;">
  <h4 style="margin:0 0 8px;color:#0369a1;">💡 How to Read This Chart:</h4>
  <ul style="margin:0;padding-left:20px;color:#1e293b;">
    <li><strong>Median line:</strong> typical return in that regime.</li>
    <li><strong>Box height:</strong> variability (wider = more dispersion).</li>
    <li><strong>Outliers:</strong> rare extreme months (tail risk).</li>
  </ul>
</div>


<div class="figure-block">
  <div id="fig05" style="width:100%; height:520px;"></div>
  <script>renderMplExport("fig05", "{{ site.baseurl }}/assets/fig_json/fig05.json");</script>
</div>

<div style="margin:20px 0;padding:16px;background:#f0f9ff;border-left:4px solid #0ea5e9;border-radius:4px;">
  <h4 style="margin:0 0 8px;color:#0369a1;">💡 How to Read This Chart:</h4>
  <ul style="margin:0;padding-left:20px;color:#1e293b;">
    <li><strong>Higher β:</strong> sector moves more than the market (more systematic risk).</li>
    <li><strong>Lower β:</strong> sector is more defensive (less market-driven).</li>
    <li><strong>Non-zero α:</strong> average performance not explained by the market factor alone.</li>
  </ul>
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
  <div id="fig07" style="width:100%; height:520px;"></div>
  <script>renderMplExport("fig07", "{{ site.baseurl }}/assets/fig_json/fig07.json");</script>
</div>

<div style="margin:20px 0;padding:16px;background:#f0f9ff;border-left:4px solid #0ea5e9;border-radius:4px;">
  <h4 style="margin:0 0 8px;color:#0369a1;">💡 How to Read This Chart:</h4>
  <ul style="margin:0;padding-left:20px;color:#1e293b;">
    <li><strong>Right side:</strong> higher market beta (more market-driven).</li>
    <li><strong>Above / below zero (y-axis):</strong> positive / negative sensitivity to Fed changes.</li>
    <li><strong>Far from the origin:</strong> sectors with the most distinctive risk profile.</li>
  </ul>
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
  <div id="fig11" style="width:100%; height:520px;"></div>
  <script>renderMplExport("fig11", "{{ site.baseurl }}/assets/fig_json/fig11.json");</script>
</div>

<div style="margin:20px 0;padding:16px;background:#f0f9ff;border-left:4px solid #0ea5e9;border-radius:4px;">
  <h4 style="margin:0 0 8px;color:#0369a1;">💡 How to Read This Chart:</h4>
  <ul style="margin:0;padding-left:20px;color:#1e293b;">
    <li><strong>Right of zero:</strong> sector outperforms the benchmark around the event window.</li>
    <li><strong>Left of zero:</strong> sector underperforms the benchmark around the event window.</li>
    <li><strong>Near zero:</strong> little average abnormal reaction.</li>
  </ul>
</div>



<div class="figure-block">
  <div id="fig12" style="width:100%; height:520px;"></div>
  <script>
    renderMplExport("fig12", "{{ site.baseurl }}/assets/fig_json/fig12.json");
  </script>
</div>

<div style="margin:20px 0;padding:16px;background:#f0f9ff;border-left:4px solid #0ea5e9;border-radius:4px;">
  <h4 style="margin:0 0 8px;color:#0369a1;">💡 How to Read This Chart:</h4>
  <ul style="margin:0;padding-left:20px;color:#1e293b;">
    <li><strong>Point estimate:</strong> average abnormal effect around the event.</li>
    <li><strong>Confidence interval:</strong> uncertainty range around that estimate.</li>
    <li><strong>Interval crosses zero:</strong> effect is not clearly different from zero.</li>
  </ul>
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
  <div id="fig02" style="width:100%; height:520px;"></div>
  <script>renderMplExport("fig02", "{{ site.baseurl }}/assets/fig_json/fig02.json");</script>
</div>

<div style="margin:20px 0;padding:16px;background:#f0f9ff;border-left:4px solid #0ea5e9;border-radius:4px;">
  <h4 style="margin:0 0 8px;color:#0369a1;">💡 How to Read This Chart:</h4>
  <ul style="margin:0;padding-left:20px;color:#1e293b;">
    <li><strong>Same direction:</strong> the two rates generally co-move (shared monetary/macro forces).</li>
    <li><strong>10Y smoother:</strong> long-term yields reflect expectations and risk premia (less “jumpy”).</li>
    <li><strong>Gaps between lines:</strong> changes in term premium / expectations about future policy.</li>
  </ul>
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
  <div id="fig03" style="width:100%; height:520px;"></div>
  <script>renderMplExport("fig03", "{{ site.baseurl }}/assets/fig_json/fig03.json");</script>
</div>

<div style="margin:20px 0;padding:16px;background:#f0f9ff;border-left:4px solid #0ea5e9;border-radius:4px;">
  <h4 style="margin:0 0 8px;color:#0369a1;">💡 How to Read This Chart:</h4>
  <ul style="margin:0;padding-left:20px;color:#1e293b;">
    <li><strong>Right of zero:</strong> returns tend to increase when the 10Y yield rises (positive sensitivity).</li>
    <li><strong>Left of zero:</strong> returns tend to fall when the 10Y yield rises (rate-sensitive / duration-like).</li>
    <li><strong>Error bar crosses zero:</strong> effect is not clearly different from zero (statistically weak).</li>
  </ul>
</div>


<div class="figure-block">
  <div id="fig08" style="width:100%; height:520px;"></div>
  <script>renderMplExport("fig08", "{{ site.baseurl }}/assets/fig_json/fig08.json");</script>
</div>

<div style="margin:20px 0;padding:16px;background:#f0f9ff;border-left:4px solid #0ea5e9;border-radius:4px;">
  <h4 style="margin:0 0 8px;color:#0369a1;">💡 How to Read This Chart:</h4>
  <ul style="margin:0;padding-left:20px;color:#1e293b;">
    <li><strong>Line position:</strong> where the yield sits relative to history.</li>
    <li><strong>Dashed thresholds:</strong> cutoffs that define “low” vs “high” rate regimes.</li>
    <li><strong>Crossing a threshold:</strong> entering a new regime used for comparison later.</li>
  </ul>
</div>


<div class="figure-block">
  <div id="fig09" style="width:100%; height:520px;"></div>
  <script>renderMplExport("fig09", "{{ site.baseurl }}/assets/fig_json/fig09.json");</script>
</div>

<div style="margin:20px 0;padding:16px;background:#f0f9ff;border-left:4px solid #0ea5e9;border-radius:4px;">
  <h4 style="margin:0 0 8px;color:#0369a1;">💡 How to Read This Chart:</h4>
  <ul style="margin:0;padding-left:20px;color:#1e293b;">
    <li><strong>Right of zero:</strong> sector performs better in the “high-rate” regime.</li>
    <li><strong>Left of zero:</strong> sector performs better in the “low-rate” regime.</li>
    <li><strong>Longer bars:</strong> larger economic difference between regimes.</li>
  </ul>
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


<!-- ===================== -->
<!-- PART 6 -->
<!-- ===================== -->

<section class="sector-part" id="part-6">

<h2>6. Volatility: do some sectors become riskier when the Fed moves?</h2>

<p class="interviewer">
<b>Interviewer:</b> Returns are one thing, but what about risk: do some sectors become more volatile when the Fed changes rates?
</p>

<h3>Context</h3>

<p>
When people say that markets “react to the Fed”, they often focus on returns, i.e. whether prices
go up or down. However, an equally important transmission channel of monetary policy is uncertainty
and risk, which manifests itself through volatility. Even when average returns do not move
substantially, the dispersion of outcomes can increase: larger price swings, deeper drawdowns,
and less stable valuations.
</p>

<p>
In this analysis, volatility is used as a proxy for risk. For a given sector, higher volatility
means that returns fluctuate more strongly within a given period, reflecting higher uncertainty
about valuation and future cash flows.
</p>

<p>
Formally, if <em>r<sub>s,d</sub></em> denotes daily returns for sector <em>s</em>, monthly realized
volatility can be defined as:
</p>

<p class="math">
σ<sub>s,m</sub> = √(∑<sub>d∈m</sub> r<sub>s,d</sub><sup>2</sup>)
</p>

<p>
An equivalent definition is the monthly standard deviation of daily returns:
</p>

<p class="math">
σ<sub>s,m</sub> = √( (1/(N<sub>m</sub>−1)) ∑<sub>d∈m</sub> (r<sub>s,d</sub> − r̄<sub>s,m</sub>)<sup>2</sup> )
</p>

<p>
Both definitions capture the same concept: higher values indicate larger typical fluctuations and
therefore higher risk.
</p>

<p>
A crucial identification challenge is that the Fed often changes rates in periods of macroeconomic
stress, when volatility is already elevated. To avoid attributing broad market fear to monetary
policy, we explicitly control for VXN, the implied volatility index for the NASDAQ-100, which serves
as a proxy for market-wide risk sentiment.
</p>

<h3>Method</h3>

<p>
We study two complementary channels through which Fed policy may affect sector volatility.
</p>

<h4>(A) Directional effect of Fed changes</h4>

<p>
We first test whether volatility reacts differently to rate hikes versus rate cuts. Let
ΔF<sub>m</sub> denote the monthly change in the Fed policy rate:
</p>

<p class="math">
ΔF<sub>m</sub> = F<sub>m</sub> − F<sub>m−1</sub>
</p>

<p>
For each sector <em>s</em>, we estimate:
</p>

<p class="math">
σ<sub>s,m</sub> = α<sub>s</sub> + β<sub>s</sub> ΔF<sub>m</sub> + δ<sub>s</sub> VXN<sub>m</sub> + ε<sub>s,m</sub>
</p>

<p>
The coefficient β<sub>s</sub> captures the signed sensitivity of sector volatility to changes in
the policy rate, conditional on overall market risk.
</p>

<h4>(B) Magnitude of Fed shocks</h4>

<p>
Markets may respond not to the direction of rate changes, but to the size of policy shocks. To test
this hypothesis, we estimate:
</p>

<p class="math">
σ<sub>s,m</sub> = α<sub>s</sub> + θ<sub>s</sub> |ΔF<sub>m</sub>| + δ<sub>s</sub> VXN<sub>m</sub> + ε<sub>s,m</sub>
</p>

<p>
Here, θ<sub>s</sub> measures how volatility responds to the absolute size of Fed moves, regardless
of sign. Inference is based on robust (HAC-type) standard errors to account for serial correlation
and heteroskedasticity in volatility.
</p>

<h3>Results</h3>

<div class="figure-block">
  <div id="fig17" style="width:100%; height:520px;"></div>
  <script>renderMplExport("fig17", "{{ site.baseurl }}/assets/fig_json/fig17.json");</script>
</div>

<div style="margin:20px 0;padding:16px;background:#f0f9ff;border-left:4px solid #0ea5e9;border-radius:4px;">
  <h4 style="margin:0 0 8px;color:#0369a1;">💡 How to Read This Chart:</h4>
  <ul style="margin:0;padding-left:20px;color:#1e293b;">
    <li><strong>Right of zero:</strong> volatility tends to rise when the Fed rate increases (hikes).</li>
    <li><strong>Left of zero:</strong> volatility tends to rise when the Fed rate decreases (cuts).</li>
    <li><strong>Error bar crosses zero:</strong> no clear directional effect once controls are included.</li>
  </ul>
</div>


<p>
Once market-wide risk (VXN) is controlled for, most sectors exhibit volatility sensitivities close
to zero, with confidence intervals overlapping zero. This suggests that the direction of Fed moves
(cuts versus hikes) does not strongly affect sector volatility on its own.
</p>

<div class="figure-block">
  <div id="fig18" style="width:100%; height:520px;"></div>
  <script>renderMplExport("fig18", "{{ site.baseurl }}/assets/fig_json/fig18.json");</script>
</div>

<div style="margin:20px 0;padding:16px;background:#f0f9ff;border-left:4px solid #0ea5e9;border-radius:4px;">
  <h4 style="margin:0 0 8px;color:#0369a1;">💡 How to Read This Chart:</h4>
  <ul style="margin:0;padding-left:20px;color:#1e293b;">
    <li><strong>Further right:</strong> volatility increases more when the Fed move is large (shock-size effect).</li>
    <li><strong>p-value labels:</strong> smaller values mean stronger statistical evidence.</li>
    <li><strong>Near zero:</strong> little or no sensitivity to shock magnitude.</li>
  </ul>
</div>



<p>
In contrast, the magnitude of Fed shocks is far more informative. Technology stands out with a large
and highly statistically significant sensitivity to |ΔFedRate|, indicating that larger policy
moves are reliably associated with higher Tech volatility. Communication Services also exhibits a
strong and significant response, followed by Energy and Basic Materials. Several other sectors show
no statistically meaningful relationship once VXN is included.
</p>

<div class="figure-block">

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

</div>

<div style="margin:20px 0;padding:16px;background:#f0f9ff;border-left:4px solid #0ea5e9;border-radius:4px;">
  <h4 style="margin:0 0 8px;color:#0369a1;">💡 How to Read This Chart:</h4>
  <ul style="margin:0;padding-left:20px;color:#1e293b;">
    <li><strong>Left axis line:</strong> monthly change in the Fed rate (policy moves over time).</li>
    <li><strong>Right axis line:</strong> sector volatility for the selected sector.</li>
    <li><strong>Look for co-movement:</strong> spikes in volatility that align with large Fed moves.</li>
  </ul>
</div>



<p>
Time-series illustrations after 2008 further support these results. Long periods of near-zero Fed
changes coexist with moderate volatility fluctuations, while sharp Fed moves coincide with visible
volatility responses in some sectors but not others, highlighting strong heterogeneity.
</p>

<h3>Conclusion</h3>

<p>
After controlling for market-wide risk, the direction of Fed changes explains little of sector
volatility. Instead, the magnitude of policy moves matters for a subset of sectors, most notably
Technology and Communication Services, with Energy and Basic Materials also affected. Volatility
responses to monetary policy are therefore sector-specific and driven primarily by shock size
rather than policy direction.
</p>

</section>

<!-- ===================== -->
<!-- PART 7 -->
<!-- ===================== -->

<section class="sector-part" id="part-7">

<h2>7. Fed vs macro confounding: naive versus controlled explanations of volatility</h2>

<p class="interviewer">
<b>Interviewer:</b> But is volatility really driven by the Fed, or is the Fed simply moving during
high-risk macroeconomic environments?
</p>

<h3>Context</h3>

<p>
A naive regression of volatility on Fed rate changes can easily attribute excessive importance to
monetary policy. The reason is structural: the Fed typically adjusts rates in response to worsening
macroeconomic conditions, which independently raise volatility across markets.
</p>

<p>
Two empirical facts must therefore be accounted for. First, volatility is persistent: high
volatility months tend to be followed by high volatility months, a phenomenon known as volatility
clustering. Second, market-wide risk conditions, captured by indices such as VXN, explain a large
fraction of sector-level volatility.
</p>

<p>
Failing to control for these effects leads to spurious Fed coefficients that primarily reflect
macro stress rather than causal monetary transmission.
</p>

<h3>Method</h3>

<h4>Naive specification</h4>

<p>
We begin with a Fed-only model:
</p>

<p class="math">
σ<sub>s,m</sub> = α<sub>s</sub> + β<sub>s</sub><sup>(N)</sup> ΔF<sub>m</sub> + ε<sub>s,m</sub>
</p>

<h4>Controlled specification</h4>

<p>
We then estimate a more complete model that accounts for macro risk and volatility persistence:
</p>

<p class="math">
σ<sub>s,m</sub> = α<sub>s</sub> + β<sub>s</sub><sup>(C)</sup> ΔF<sub>m</sub> + δ<sub>s</sub> VXN<sub>m</sub>
+ ∑<sub>k=1</sub><sup>K</sup> φ<sub>s,k</sub> σ<sub>s,m−k</sub> + η<sub>s,m</sub>
</p>

<p>
Inference relies on heteroskedasticity- and autocorrelation-consistent standard errors.
</p>

<h4>Explained variance comparison</h4>

<p>
We compare explanatory power using R²:
</p>

<p class="math">
ΔR² = R²<sub>controlled</sub> − R²<sub>naive</sub>
</p>

<p>
Finally, total explained variance is decomposed into macro risk plus volatility persistence versus
the incremental contribution of the Fed given those controls.
</p>

<h3>Results</h3>

<div class="figure-block">
  <div id="fig20" style="width:100%; height:560px;"></div>
  <script>renderMplExport("fig20", "{{ site.baseurl }}/assets/fig_json/fig20.json");</script>
</div>


<div style="margin:20px 0;padding:16px;background:#f0f9ff;border-left:4px solid #0ea5e9;border-radius:4px;">
  <h4 style="margin:0 0 8px;color:#0369a1;">💡 How to Read This Chart:</h4>
  <ul style="margin:0;padding-left:20px;color:#1e293b;">
    <li><strong>Two dots per sector:</strong> naive estimate vs controlled estimate.</li>
    <li><strong>Big gap between dots:</strong> strong confounding (macro risk explains the naive effect).</li>
    <li><strong>Controlled dot near zero:</strong> little incremental Fed effect after controls.</li>
  </ul>
</div>


<p>
In the naive specification, Fed coefficients are large and often strongly negative, reflecting the
fact that rate cuts tend to occur during high-volatility episodes. Once macro risk and volatility
persistence are controlled for, these coefficients shrink dramatically and often move close to
zero, indicating substantial confounding in the naive estimates.
</p>

<div class="figure-block">
  <div id="fig21" style="width:100%; height:520px;"></div>
  <script>
    renderMplExport("fig21", "{{ site.baseurl }}/assets/fig_json/fig21.json");
  </script>
</div>


<div style="margin:20px 0;padding:16px;background:#f0f9ff;border-left:4px solid #0ea5e9;border-radius:4px;">
  <h4 style="margin:0 0 8px;color:#0369a1;">💡 How to Read This Chart:</h4>
  <ul style="margin:0;padding-left:20px;color:#1e293b;">
    <li><strong>Higher values:</strong> controls (macro risk + persistence) explain much more volatility.</li>
    <li><strong>Near zero:</strong> controls add little explanatory power for that sector.</li>
    <li><strong>Comparing sectors:</strong> which sectors are most dominated by macro/persistence dynamics.</li>
  </ul>
</div>


<p>
Adding VXN and volatility persistence leads to large increases in explanatory power across all
sectors. The gain in R² is substantial, confirming that macro conditions and volatility clustering
dominate sector-level volatility dynamics.
</p>

<div class="figure-block">
  <div id="fig22" style="width:100%; height:700px;"></div>
  <script>
    renderMplExport("fig22", "{{ site.baseurl }}/assets/fig_json/fig22.json");
  </script>
</div>


<div style="margin:20px 0;padding:16px;background:#f0f9ff;border-left:4px solid #0ea5e9;border-radius:4px;">
  <h4 style="margin:0 0 8px;color:#0369a1;">💡 How to Read This Chart:</h4>
  <ul style="margin:0;padding-left:20px;color:#1e293b;">
    <li><strong>Main bar segment:</strong> variance explained by macro risk and volatility persistence.</li>
    <li><strong>Smaller added segment:</strong> extra variance explained by the Fed after controls.</li>
    <li><strong>Star marker:</strong> statistically detectable incremental Fed contribution (if present).</li>
  </ul>
</div>


<p>
Variance decomposition shows that macro risk and volatility persistence account for the vast
majority of explained variance. The incremental Fed contribution, while sometimes statistically
detectable, is quantitatively small for all sectors.
</p>

<h3>Conclusion</h3>

<p>
A naive analysis overstates the role of monetary policy in driving sector volatility. Once macro
conditions and volatility persistence are properly accounted for, the Fed’s incremental
contribution is small and sector-dependent. Sector volatility is primarily a macroeconomic
phenomenon, with monetary policy acting as a secondary amplifier rather than a dominant driver.
</p>

</section>





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
