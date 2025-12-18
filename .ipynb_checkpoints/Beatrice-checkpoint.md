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

<div id="fig13" style="width:100%; height:520px;"></div>
<script>renderMplExport("fig13", "{{ site.baseurl }}/assets/fig_json/fig13.json");</script>

<div id="fig14" style="width:100%; height:520px;"></div>
<script>renderMplExport("fig14", "{{ site.baseurl }}/assets/fig_json/fig14.json");</script>

<div id="fig15" style="width:100%; height:520px;"></div>
<script>renderMplExport("fig15", "{{ site.baseurl }}/assets/fig_json/fig15.json");</script>

<div id="fig16" style="width:100%; height:520px;"></div>
<script>renderMplExport("fig16", "{{ site.baseurl }}/assets/fig_json/fig16.json");</script>

<div id="fig17" style="width:100%; height:520px;"></div>
<script>renderMplExport("fig17", "{{ site.baseurl }}/assets/fig_json/fig17.json");</script>

<div id="fig18" style="width:100%; height:520px;"></div>
<script>renderMplExport("fig18", "{{ site.baseurl }}/assets/fig_json/fig18.json");</script>

<div id="fig19" style="width:100%; height:520px;"></div>
<script>renderMplExport("fig19", "{{ site.baseurl }}/assets/fig_json/fig19.json");</script>

<div id="fig20" style="width:100%; height:520px;"></div>
<script>renderMplExport("fig20", "{{ site.baseurl }}/assets/fig_json/fig20.json");</script>

<div id="fig21" style="width:100%; height:520px;"></div>
<script>renderMplExport("fig21", "{{ site.baseurl }}/assets/fig_json/fig21.json");</script>

<div id="fig22" style="width:100%; height:520px;"></div>
<script>renderMplExport("fig22", "{{ site.baseurl }}/assets/fig_json/fig22.json");</script>





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
