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
If you only look at a market index, you implicitly assume that all firms react in roughly the same
way to macroeconomic forces. In practice, sectors differ in capital intensity, leverage, pricing
power, exposure to rates, and how much their value depends on future growth.
</p>
<p>
So, to respond to your question, a good starting point is to separate two things: what is simply
the market moving up and down, and what is genuinely sector-specific behavior. If sector paths
diverge even after you account for the market, then it makes sense to study additional drivers
later, like monetary policy.
</p>
<p>
The baseline question we want to answer here is very simple: do sectors mostly look like scaled
versions of the market, or do they have their own long-run trajectories?
</p>

<div style="margin:14px 0;padding:14px;background:#fff7ed;border-left:4px solid #fb923c;border-radius:4px;">
  <h4 style="margin:0 0 8px;color:#9a3412;">🎮 Easy game question (Part 1)</h4>
  <p style="margin:0;color:#7c2d12;">
    If two sectors have the same market beta β but very different cumulative returns over time, what does it suggest?
    (A) The market explains everything (B) Sector-specific factors matter (C) Returns are random
  </p>
</div>

<h3>Method</h3>

<p>
To respond to this question, you could begin by defining a consistent measure of performance.
Prices are not directly comparable across sectors because they have different levels and scales, so
the first step is to work with returns, which normalize changes over time.
</p>
<p>
A practical choice is log-returns because they add nicely over time and are standard in finance.
That gives you a clean daily or monthly return series per sector.
</p>

For each sector s, we compute log-returns:

<blockquote style="margin:16px 0;padding:12px 16px;border-left:4px solid #cbd5e1;background:#f8fafc;">
  <img
    src="https://latex.codecogs.com/svg.image?r_{s,t}=\ln\!\left(\frac{P_{s,t}}{P_{s,t-1}}\right)"
    style="max-width:380px;height:auto;display:block;"
    alt="log returns"
  >
  <p style="margin:8px 0 0;font-style:italic;font-size:0.95em;">
    With rₛ,ₜ the log-return of sector <b>s</b> at time <b>t</b>.
  </p>
</blockquote>

<p>
Then, to visualize long-run differences, you can compound these returns. This turns a noisy return
series into an interpretable performance curve: if you start at 1, where does each sector end up?
</p>

Returns are aggregated into cumulative returns rebased to 1:

<blockquote style="margin:16px 0;padding:12px 16px;border-left:4px solid #cbd5e1;background:#f8fafc;">
  <img
    src="https://latex.codecogs.com/svg.image?CR_{s,t}=\prod_{\tau\le t}(1+r_{s,\tau})"
    style="max-width:420px;height:auto;display:block;"
    alt="cumulative returns"
  >
  <p style="margin:8px 0 0;font-style:italic;font-size:0.95em;">
    Cumulative return rebased to 1, obtained by compounding sector returns over time.
  </p>
</blockquote>

<p>
Finally, if you want to quantify how much a sector is just following the market, you can estimate
a simple market model. Intuitively, you try to explain sector returns by market returns. What is
left in the residual is the part not captured by broad market movement.
</p>

<p>
To isolate sector-specific behavior, we estimate a CAPM-style market model:
</p>

<blockquote style="margin:16px 0;padding:12px 16px;border-left:4px solid #cbd5e1;background:#f8fafc;">
  <img
    src="https://latex.codecogs.com/svg.image?r_{s,t}=\alpha_s+\beta_s r_{m,t}+\varepsilon_{s,t}"
    style="max-width:420px;height:auto;display:block;"
    alt="CAPM model"
  >
  <p style="margin:8px 0 0;font-style:italic;font-size:0.95em;">
    βₛ measures exposure to market risk, while αₛ captures average excess performance.
  </p>
</blockquote>

<h3>Results</h3>

<p>
Here, what we are trying to see is whether sectors share the same long-run trend, or whether their
performance separates into persistent winners and laggards. Then we want to check whether this
dispersion is simply explained by market exposure β or not.
</p>

<p><b>In Fig.1, we want to</b> visually compare long-run cumulative performance across sectors.</p>

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

<p>
What you typically observe in this kind of plot is that sectors do not simply move together with a
constant gap. Instead, dispersion often widens in major episodes, suggesting that shocks and
regimes do not impact sectors proportionally. If a few curves permanently pull away from others,
that tells you the differences are structural rather than short-lived noise.
</p>

<p><b>In Fig.4, we want to</b> check how the distribution of returns changes across regimes, focusing on dispersion and tail events.</p>

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

<p>
When the boxes widen or outliers become more frequent, it indicates that the regime is not just
changing the average return, but also changing risk and dispersion. This is important because it
motivates later parts of the analysis that focus on volatility and event windows.
</p>

<p><b>In Fig.5, we want to</b> quantify how market-driven each sector is through β, and whether there is systematic outperformance through α.</p>

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
If you see large differences in β across sectors, that is already a strong reason to avoid using
only a single market index. More importantly, if some sectors show persistent deviations that are
not aligned with β, that suggests market exposure is not the full story. That sets up the next
question: beyond the market factor, how much does monetary policy matter?
</p>

<h3>Conclusion</h3>
<p>
So the takeaway is: to respond to your original question, sector-level analysis is useful because
it reveals persistent dispersion. Market exposure explains a lot, but it does not fully explain the
relative trajectories, which motivates adding monetary policy variables in later parts.
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
To respond to that, you can think of the Fed rate as affecting both discount rates and financing
conditions. But those channels vary by sector: some sectors rely heavily on external funding and
long-horizon growth, while others are more cash-flow stable or benefit from different macro
conditions.
</p>
<p>
So what we want to test here is whether the sensitivity to Fed changes is homogeneous. If it is
not, that gives a sector-level transmission mechanism of monetary policy.
</p>

<div style="margin:14px 0;padding:14px;background:#fff7ed;border-left:4px solid #fb923c;border-radius:4px;">
  <h4 style="margin:0 0 8px;color:#9a3412;">🎮 Easy game question (Part 2)</h4>
  <p style="margin:0;color:#7c2d12;">
    If a sector has high market beta β but γ close to zero, what does it mean?
    (A) It follows the market but is not especially Fed-sensitive (B) It is strongly Fed-sensitive (C) It is risk-free
  </p>
</div>

<h3>Method</h3>

<p>
To answer this, you want to isolate Fed effects from general market movement. If you do not
control for the market, you might confuse a broad market day with a policy effect. So the idea is
to regress sector returns on both market returns and Fed rate changes.
</p>

We estimate sector-specific regressions controlling for market movements:

<blockquote style="margin:16px 0;padding:12px 16px;border-left:4px solid #cbd5e1;background:#f8fafc;">
  <img
    src="https://latex.codecogs.com/svg.image?r_{s,t}=\alpha_s+\beta_s r_{m,t}+\gamma_s\Delta FedRate_t+u_{s,t}"
    style="max-width:440px;height:auto;display:block;"
    alt="market plus fed regression"
  >
  <p style="margin:8px 0 0;font-style:italic;font-size:0.95em;">
    γₛ measures the marginal sensitivity of sector returns to changes in the Fed policy rate.
  </p>
</blockquote>

<h3>Results</h3>

<p>
Here, what we are trying to see is whether Fed sensitivity γ lines up with market beta β, or
whether it is an independent dimension of sector risk. In other words, do the sectors that are
market-driven also happen to be policy-sensitive, or not?
</p>

<p><b>In Fig.7, we want to</b> locate sectors in a two-dimensional map: market exposure on one axis and Fed sensitivity on the other.</p>

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
What you look for is whether points spread vertically a lot. A wide vertical spread means sectors
react differently to Fed changes even if they have similar market exposure. That supports the idea
that policy sensitivity is not just a re-labeling of market risk, but an additional channel.
</p>

<h3>Conclusion</h3>
<p>
So to respond to your question: no, sectors are not equally sensitive. Once you control for the
market, you still see heterogeneity in γ, meaning monetary policy contributes a sector-specific
risk dimension beyond market beta.
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
To respond to that, it helps to separate expected moves from surprises. If a move is fully priced
in, returns may barely react. But a surprise cut often conveys information about stress or
deteriorating conditions. So the market reaction can reflect the signal, not only the mechanical
impact of lower rates.
</p>

<div style="margin:14px 0;padding:14px;background:#fff7ed;border-left:4px solid #fb923c;border-radius:4px;">
  <h4 style="margin:0 0 8px;color:#9a3412;">🎮 Easy game question (Part 3)</h4>
  <p style="margin:0;color:#7c2d12;">
    If most sectors have negative abnormal returns around a surprise rate cut, what is the most likely interpretation?
    (A) The cut is good news (B) The cut signals bad macro conditions (C) Markets ignore surprises
  </p>
</div>

<h3>Method</h3>

<p>
To answer this, you can use an event-study. The intuition is: instead of looking at long windows
where many things happen, you zoom into a short window around the policy surprise and compare the
sector to a benchmark. That reduces contamination from other slow-moving factors.
</p>

We implement a short-horizon event-study framework around surprise Fed cuts. Sector performance is
measured relative to a benchmark sector (Industrials):

<blockquote style="margin:16px 0;padding:12px 16px;border-left:4px solid #cbd5e1;background:#f8fafc;">
  <img
    src="https://latex.codecogs.com/svg.image?AR_{s,t}=r_{s,t}-r_{Ind,t}"
    style="max-width:360px;height:auto;display:block;"
    alt="abnormal returns"
  >
  <p style="margin:8px 0 0;font-style:italic;font-size:0.95em;">
    Abnormal return of sector <b>s</b> measured relative to the Industrials benchmark.
  </p>
</blockquote>

<h3>Results</h3>

<p>
Here, what we are trying to see is whether surprise cuts produce consistent sector winners and
losers, which would indicate that the informational content of the decision matters and differs by
sector.
</p>

<p><b>In Fig.11, we want to</b> compare average abnormal performance across sectors during the event window.</p>

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

<p>
If many bars sit left of zero, that suggests the event is interpreted as negative news overall. If
some sectors sit clearly on the right while others sit on the left, that indicates heterogeneity
in how sectors map macro stress into expected cash flows.
</p>

<p><b>In Fig.12, we want to</b> check which sector effects are clearly different from zero once uncertainty is accounted for.</p>

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
Here the key is whether confidence intervals cross zero. If they do, you cannot confidently claim
a directional effect for that sector in the event window. If some sectors remain clearly negative
even with uncertainty, that strengthens the interpretation that surprise easing often signals
stress rather than relief.
</p>

<h3>Conclusion</h3>
<p>
So to respond to your question: yes, sectors react differently to surprises, and the pattern often
supports a signaling story. The event-study helps isolate that short-run informational effect.
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
To respond to that, you want to match the horizon of the financial variable to the horizon of
equity valuation. Stocks are long-duration assets: prices depend on discounting cash flows far in
the future. The Fed Funds Rate is a short-term policy tool, while long-term yields embed expected
future policy, inflation expectations, and term premia.
</p>

<div style="margin:14px 0;padding:14px;background:#fff7ed;border-left:4px solid #fb923c;border-radius:4px;">
  <h4 style="margin:0 0 8px;color:#9a3412;">🎮 Easy game question (Part 4)</h4>
  <p style="margin:0;color:#7c2d12;">
    Which rate is usually more forward-looking for long-horizon valuation: the Fed Funds rate or the 10-year yield?
    (A) Fed Funds (B) 10-year yield (C) Neither
  </p>
</div>

<h3>Method</h3>
<p>
A simple way to answer is to plot both series and look at how they co-move. The intuition is that
if you want a long-run proxy for monetary conditions relevant to equity valuation, you prefer the
series that moves with policy but is smoother and expectation-driven.
</p>
<p>
We compare the dynamics of the Fed Funds Rate and the 10-year Treasury yield, and use the latter as
a proxy for long-term monetary conditions.
</p>

<h3>Results</h3>

<p>
Here, what we are trying to see is whether the 10-year yield tracks the broad stance of policy
while filtering out short-term noise, which makes it a more stable signal for long-horizon sector
analysis.
</p>

<p><b>In Fig.2, we want to</b> visually assess co-movement and whether the 10Y behaves like a smoother, expectation-based version of policy stance.</p>

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
If the two series broadly track each other but the 10Y is smoother, it supports using the 10Y as a
long-horizon proxy. When gaps open, that can reflect changing expectations or term premia, which is
exactly the kind of information relevant for valuing long-duration assets.
</p>

<h3>Conclusion</h3>
<p>
So to respond to your question: the Fed rate is informative for short-term actions, but the 10-year
yield is often the better long-run proxy because it embeds expectations and is less noisy.
</p>

</section>

<!-- ===================== -->
<!-- PART 5 -->
<!-- ===================== -->

<section class="sector-part" id="part-5">

<h2>5. Which sectors perform better in high-rate environments?</h2>

<p class="interviewer">
<b>Interviewer:</b> Which sectors benefit or suffer when long-term interest rates are high?
</p>

<h3>Context</h3>
<p>
To respond to that, you can think of high-rate environments as changing both discounting and the
macro mix. Sectors with long-duration cash flows tend to be hurt more when discount rates rise,
while sectors linked to commodities, financial intermediation, or pricing power may behave
differently.
</p>

<div style="margin:14px 0;padding:14px;background:#fff7ed;border-left:4px solid #fb923c;border-radius:4px;">
  <h4 style="margin:0 0 8px;color:#9a3412;">🎮 Easy game question (Part 5)</h4>
  <p style="margin:0;color:#7c2d12;">
    If a sector has negative sensitivity to the 10Y yield, what usually happens when yields rise?
    (A) Sector tends to fall (B) Sector tends to rise (C) No relationship
  </p>
</div>

<h3>Method</h3>
<p>
To answer this, you can do two complementary things. First, estimate a regression that links
sector returns to changes in the 10-year yield while still controlling for the market. Second,
define regimes, for example “low” and “high” yield months, and compare average sector performance
across regimes. The regression gives a marginal sensitivity, and the regime approach gives a more
economic comparison.
</p>

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

<p>
Here, what we are trying to see is whether some sectors behave like “rate beneficiaries” while
others behave like “rate victims”. We also want to see whether the regime differences are large in
economic terms, not only statistically.
</p>

<p><b>In Fig.3, we want to</b> estimate which sectors have positive or negative sensitivity to changes in the 10Y yield.</p>

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

<p>
The key thing to look at is which sectors have estimates clearly left of zero with error bars that
do not cross zero. Those are the sectors most likely to be structurally rate-sensitive. Sectors on
the right are candidates for sectors that benefit in higher-yield environments, or at least are
not penalized by higher discount rates.
</p>

<p><b>In Fig.8, we want to</b> define low and high yield regimes using thresholds, so we can compare average performance between regimes.</p>

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

<p>
This plot matters because the regime definition is only as good as the threshold separation. If
the series spends meaningful time in both regimes, your comparison has enough data. If it rarely
enters one regime, regime comparisons become noisy.
</p>

<p><b>In Fig.9, we want to</b> quantify economic differences: which sectors have meaningfully higher average returns in high-rate months versus low-rate months.</p>

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
Here you want to compare the sign and the magnitude. A small bar may be statistically detectable
but economically minor. A large bar suggests a meaningful regime effect. If the sectors that look
rate-sensitive in Fig. 3 also show large regime differences here, that gives a coherent story.
</p>

<h3>Conclusion</h3>
<p>
So to respond to your question: high rates do not uniformly depress equities. Instead, they are
associated with systematic sector rotation, where some sectors do relatively better and others do
worse, which is exactly why the sector view is necessary.
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
To respond to that, you can shift from average returns to risk. Even if average returns do not
move much, policy can change uncertainty. More uncertainty shows up as higher volatility: prices
swing more, drawdowns can deepen, and the range of outcomes widens.
</p>

<p>
Volatility is not just noise. In finance it is a practical proxy for risk because it measures how
unstable returns are over time.
</p>

<div style="margin:14px 0;padding:14px;background:#fff7ed;border-left:4px solid #fb923c;border-radius:4px;">
  <h4 style="margin:0 0 8px;color:#9a3412;">🎮 Easy game question (Part 6)</h4>
  <p style="margin:0;color:#7c2d12;">
    If a sector’s volatility rises when |ΔFedRate| is large, what does it mean?
    (A) Big Fed moves increase uncertainty for that sector (B) Fed moves reduce risk (C) Volatility is unrelated to policy
  </p>
</div>

<p>
Formally, if <em>r<sub>s,d</sub></em> denotes daily returns for sector <em>s</em>, monthly realized
volatility can be defined as:
</p>

<blockquote style="margin:16px 0;padding:12px 16px;border-left:4px solid #cbd5e1;background:#f8fafc;">
  <img
    src="https://latex.codecogs.com/svg.image?\sigma_{s,m}=\sqrt{\sum_{d\in m}r_{s,d}^2}"
    style="max-width:420px;height:auto;display:block;"
    alt="realized volatility"
  >
  <p style="margin:8px 0 0;font-style:italic;font-size:0.95em;">
    Monthly realized volatility computed from daily sector returns.
  </p>
</blockquote>

<p>
An equivalent definition is the monthly standard deviation of daily returns:
</p>

<blockquote style="margin:16px 0;padding:12px 16px;border-left:4px solid #cbd5e1;background:#f8fafc;">
  <img
    src="https://latex.codecogs.com/svg.image?\sigma_{s,m}=\sqrt{\frac{1}{N_m-1}\sum_{d\in m}(r_{s,d}-\bar r_{s,m})^2}"
    style="max-width:440px;height:auto;display:block;"
    alt="volatility standard deviation"
  >
  <p style="margin:8px 0 0;font-style:italic;font-size:0.95em;">
    Equivalent definition of volatility as the standard deviation of daily returns.
  </p>
</blockquote>

<p>
A key methodological point is confounding: the Fed tends to move during stress, and stress raises
volatility everywhere. So to avoid attributing broad fear to policy, you control for VXN, which
captures market-wide risk sentiment.
</p>

<h3>Method</h3>

<p>
To answer your question, you can test two separate ideas. First, does the direction of policy
matter, meaning hikes versus cuts. Second, does the magnitude matter, meaning large moves versus
small moves. In both cases, you include VXN to separate macro fear from policy effects.
</p>

<p>
We study two complementary channels through which Fed policy may affect sector volatility.
</p>


<h4>(A) Directional effect of Fed changes</h4>

<p>
We first test whether volatility reacts differently to rate hikes versus rate cuts. Let
ΔF<sub>m</sub> denote the monthly change in the Fed policy rate:
</p>

<blockquote style="margin:16px 0;padding:12px 16px;border-left:4px solid #cbd5e1;background:#f8fafc;">
  <img
    src="https://latex.codecogs.com/svg.image?\Delta F_m=F_m-F_{m-1}"
    style="max-width:300px;height:auto;display:block;"
    alt="fed rate change"
  >
  <p style="margin:8px 0 0;font-style:italic;font-size:0.95em;">
    Monthly change in the Fed policy rate.
  </p>
</blockquote>

<p>
For each sector <em>s</em>, we estimate:
</p>

<blockquote style="margin:16px 0;padding:12px 16px;border-left:4px solid #cbd5e1;background:#f8fafc;">
  <img
    src="https://latex.codecogs.com/svg.image?\sigma_{s,m}=\alpha_s+\beta_s\Delta F_m+\delta_s VXN_m+\varepsilon_{s,m}"
    style="max-width:460px;height:auto;display:block;"
    alt="volatility regression with fed direction"
  >
  <p style="margin:8px 0 0;font-style:italic;font-size:0.95em;">
    βₛ captures the signed response of sector volatility to Fed rate changes (controlling for VXN).
  </p>
</blockquote>

<h4>(B) Magnitude of Fed shocks</h4>

<p>
Markets may respond not to the direction of rate changes, but to the size of policy shocks. To test
this hypothesis, we estimate:
</p>

<blockquote style="margin:16px 0;padding:12px 16px;border-left:4px solid #cbd5e1;background:#f8fafc;">
  <img
    src="https://latex.codecogs.com/svg.image?\sigma_{s,m}=\alpha_s+\theta_s\left|\Delta F_m\right|+\delta_s VXN_m+\varepsilon_{s,m}"
    style="max-width:460px;height:auto;display:block;"
    alt="volatility magnitude"
  >
  <p style="margin:8px 0 0;font-style:italic;font-size:0.95em;">
    θₛ measures how volatility reacts to the size of Fed moves (ignoring direction), controlling for VXN.
  </p>
</blockquote>

<p>
Inference is based on robust (HAC-type) standard errors to account for serial correlation
and heteroskedasticity in volatility.
</p>
   

<h3>Results</h3>

<p>
Here, what we are trying to see is whether Fed policy has any incremental relationship with
sector volatility once you control for market-wide fear. First we test direction, then magnitude,
then we use a time-series view to see how the relationship looks through time.
</p>

<p><b>In Fig.17, we want to</b> test whether volatility responds differently to hikes versus cuts after controlling for VXN.</p>

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
If most estimates sit close to zero and confidence intervals cross zero, the practical conclusion
is that direction is not a robust predictor once broad market risk is accounted for. That is often
what you expect if the main driver is macro stress rather than the sign of the policy move.
</p>

<p><b>In Fig.18, we want to</b> test whether large policy moves, regardless of sign, are associated with higher volatility in some sectors.</p>

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
What you typically see here is stronger sector separation: a subset of sectors show positive
sensitivity to shock size with small p-values, while many sectors cluster near zero. That pattern
supports a story where only some sectors treat large policy moves as a meaningful uncertainty
signal, while others do not.
</p>

<p><b>In Fig.19, we want to</b> visually check co-movement over time: do volatility spikes align with large Fed changes in the chosen sector?</p>

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
This plot is a sanity check. If you pick a sector that showed strong sensitivity in Fig. 18, you
often see volatility spikes lining up with large policy moves in crisis periods. If you pick a
sector with near-zero sensitivity, you usually see volatility moving without clear alignment to Fed
moves, which supports the heterogeneity story.
</p>

<h3>Conclusion</h3>

<p>
So to respond to your original question: once you control for market-wide risk, direction explains
little. The magnitude of moves matters for some sectors, which suggests policy shocks act more like
an uncertainty amplifier for particular sector structures.
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
To respond to that, you should explicitly test confounding. The Fed often moves when the economy
deteriorates. Those same periods raise volatility through risk sentiment, leverage constraints,
liquidity stress, and uncertainty. If you regress volatility only on Fed changes, you may just be
capturing crisis timing.
</p>

<p>
Two stylized facts matter. Volatility is persistent, meaning high volatility tends to follow high
volatility. And market-wide risk indices like VXN explain a large share of what happens in sector
volatility.
</p>

<div style="margin:14px 0;padding:14px;background:#fff7ed;border-left:4px solid #fb923c;border-radius:4px;">
  <h4 style="margin:0 0 8px;color:#9a3412;">🎮 Easy game question (Part 7)</h4>
  <p style="margin:0;color:#7c2d12;">
    If the Fed coefficient becomes much smaller after adding VXN and lagged volatility, what does it suggest?
    (A) Confounding was inflating the naive Fed effect (B) The Fed effect gets stronger (C) Controls are irrelevant
  </p>
</div>

<h3>Method</h3>

<p>
To answer this, you can compare two models. First a naive model that uses only Fed changes. Then a
controlled model that adds macro risk (VXN) and volatility persistence through lagged volatility.
The intuition is: if the Fed coefficient collapses when you add those controls, the naive effect
was mostly picking up macro stress timing.
</p>

<h4>Naive specification</h4>

<p>
We begin with a Fed-only model:
</p>

<blockquote style="margin:16px 0;padding:12px 16px;border-left:4px solid #cbd5e1;background:#f8fafc;">
  <img
    src="https://latex.codecogs.com/svg.image?\sigma_{s,m}=\alpha_s+\beta_s^{(N)}\Delta F_m+\varepsilon_{s,m}"
    style="max-width:420px;height:auto;display:block;"
    alt="naive volatility"
  >
  <p style="margin:8px 0 0;font-style:italic;font-size:0.95em;">
    Naive specification that ignores macro risk and volatility persistence.
  </p>
</blockquote>

<h4>Controlled specification</h4>

<p>
We then estimate a more complete model that accounts for macro risk and volatility persistence:
</p>

<blockquote style="margin:16px 0;padding:12px 16px;border-left:4px solid #cbd5e1;background:#f8fafc;">
  <img
    src="https://latex.codecogs.com/svg.image?\sigma_{s,m}=\alpha_s+\beta_s^{(C)}\Delta F_m+\delta_s VXN_m+\sum_{k=1}^K\phi_{s,k}\sigma_{s,m-k}+\eta_{s,m}"
    style="max-width:460px;height:auto;display:block;"
    alt="controlled volatility"
  >
  <p style="margin:8px 0 0;font-style:italic;font-size:0.95em;">
    Controlled model accounting for macro risk and volatility persistence.
  </p>
</blockquote>

<p>
Inference relies on heteroskedasticity- and autocorrelation-consistent standard errors.
</p>

<h4>Explained variance comparison</h4>

<p>
We compare explanatory power using R². Intuitively, if the controlled model explains much more,
that tells you macro risk and persistence dominate volatility dynamics.
</p>

<blockquote style="margin:16px 0;padding:12px 16px;border-left:4px solid #cbd5e1;background:#f8fafc;">
  <img
    src="https://latex.codecogs.com/svg.image?\Delta R^2=R^2_{\text{controlled}}-R^2_{\text{naive}}"
    style="max-width:340px;height:auto;display:block;"
    alt="delta r2"
  >
  <p style="margin:8px 0 0;font-style:italic;font-size:0.95em;">
    Increase in explanatory power when macro controls are included.
  </p>
</blockquote>

<p>
Finally, total explained variance is decomposed into macro risk plus volatility persistence versus
the incremental contribution of the Fed given those controls.
</p>

<h3>Results</h3>

<p>
Here, what we are trying to see is three things: whether naive Fed coefficients are exaggerated,
how much explanatory power comes from macro risk and persistence, and whether the Fed adds anything
material after those controls.
</p>

<p><b>In Fig.20, we want to</b> visually compare naive versus controlled Fed coefficients sector by sector.</p>

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
If controlled dots cluster near zero while naive dots are far away, the interpretation is that the
Fed variable in the naive model is acting as a proxy for crisis timing. The controlled model strips
out that timing using VXN and persistence, so what remains is closer to an incremental policy
effect.
</p>

<p><b>In Fig.21, we want to</b> measure how much explanatory power is added when including macro risk and volatility persistence.</p>

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
A strong ΔR² across sectors means the controlled model captures the dominant drivers of volatility.
If ΔR² is large and common across sectors, that supports the view that volatility is largely a
macro regime phenomenon plus persistence rather than a direct response to policy changes.
</p>

<p><b>In Fig.22, we want to</b> decompose explained variance into what comes from macro risk and persistence versus what is added by the Fed on top.</p>

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
If the macro plus persistence segment dominates and the Fed segment is consistently small, the
practical conclusion is that the Fed adds limited incremental explanatory power once you account
for the macro environment. Stars can indicate detectability, but you should still compare sizes,
because a statistically detectable effect can still be economically small.
</p>

<h3>Conclusion</h3>

<p>
So to respond to your question: yes, macro confounding is a major issue. A naive model overstates
the Fed role because the Fed moves during stress. After controls, the Fed contribution is smaller
and sector-dependent, with volatility driven mainly by macro risk and persistence.
</p>

</section>






<!--


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

-->
