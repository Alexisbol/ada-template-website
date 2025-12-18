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

      /* =========================
         DATAFRAME EXPORTS
         ========================= */

      // line (NOT stacked)
    
    if (d.type === "dataframe" && d.kind === "line") {
      const traces = d.series.map(s => ({
        x: d.x, y: s.y, name: s.name, type: "scatter", mode: "lines"
      }));
      Plotly.newPlot(divId, traces, {...}, {responsive:true});
      return;
    }
    
    if (d.type === "dataframe" && d.kind === "stacked") {
      const traces = d.series.map(s => ({
        x: d.x, y: s.y, name: s.name, type: "scatter", mode: "lines", stackgroup: "one"
      }));
      Plotly.newPlot(divId, traces, {...}, {responsive:true});
      return;
    }


      // boxplot (fig04)
      if (d.type === "dataframe" && d.kind === "box") {
        Plotly.newPlot(divId, [{
          x: d.categories, y: d.values, type: "box", boxpoints: "outliers"
        }], {
          title: d.title || "",
          yaxis: { title: d.ylabel || "" }
        }, { responsive: true });
        return;
      }

      // errorbar horizontal (fig03-style) — accepts either "errorbar" or "errorbar_h_zero"
      if (d.type === "dataframe" && (d.kind === "errorbar" || d.kind === "errorbar_h_zero")) {
        Plotly.newPlot(divId, [{
          x: d.x, y: d.categories,
          type: "scatter", mode: "markers",
          error_x: { type: "data", symmetric: false, array: d.xerr_high, arrayminus: d.xerr_low }
        }], {
          title: d.title || "",
          xaxis: { title: d.xlabel || "", zeroline: true }
        }, { responsive: true });
        return;
      }

      // scatter + labels (fig07)
      if (d.type === "dataframe" && d.kind === "scatter_label") {
        Plotly.newPlot(divId, [{
          x: d.points.map(p => p.x),
          y: d.points.map(p => p.y),
          text: d.points.map(p => p.name),
          mode: "markers+text",
          textposition: "top center",
          type: "scatter"
        }], {
          title: d.title || "",
          xaxis: { title: d.xlabel || "Market beta (NASDAQ)", zeroline: true },
          yaxis: { title: d.ylabel || "", zeroline: true }
        }, { responsive: true });
        return;
      }

      // line + thresholds (fig08)
      if (d.type === "dataframe" && d.kind === "line_thresholds") {
        const traces = [{
          x: d.x,
          y: d.series[0].y,
          name: d.series[0].name || "Series",
          type: "scatter",
          mode: "lines",
          line: { width: 2 }
        }];
        (d.thresholds || []).forEach(t => {
          const y = (typeof t === "number") ? t : t.y;
          const name = (typeof t === "number") ? "threshold" : (t.label || "threshold");
          const color = (typeof t === "number") ? undefined : (t.color || undefined);
          traces.push({
            x: [d.x[0], d.x[d.x.length - 1]],
            y: [y, y],
            type: "scatter",
            mode: "lines",
            name,
            line: { dash: "dash", color }
          });
        });
        Plotly.newPlot(divId, traces, {
          title: d.title || "",
          xaxis: { title: d.xlabel || "" },
          yaxis: { title: d.ylabel || "" }
        }, { responsive: true });
        return;
      }

      // barh + zero line (fig09 / fig11)
      if (d.type === "dataframe" && d.kind === "barh_zero") {
        Plotly.newPlot(divId, [{
          x: d.values, y: d.categories,
          type: "bar", orientation: "h"
        }], {
          title: d.title || "",
          xaxis: { title: d.xlabel || "", zeroline: true },
          shapes: [{
            type: "line",
            x0: d.zero_line ?? 0, x1: d.zero_line ?? 0,
            y0: -0.5, y1: d.categories.length - 0.5,
            line: { color: "black", width: 1, dash: "dash" }
          }]
        }, { responsive: true });
        return;
      }

      // barh + hover pvalue (if you used it)
      if (d.type === "dataframe" && d.kind === "barh_hover_pvalue") {
        const hoverText = d.categories.map((c, i) =>
          `${c}<br>High − Low: ${Number(d.values[i]).toFixed(2)}% per year<br>p-value: ${Number(d.p_values[i]).toExponential(2)}`
        );
        Plotly.newPlot(divId, [{
          x: d.values, y: d.categories,
          type: "bar", orientation: "h",
          hovertext: hoverText, hoverinfo: "text"
        }], {
          title: d.title || "",
          xaxis: { title: d.xlabel || "", zeroline: true }
        }, { responsive: true });
        return;
      }

      /* =========================
         MATPLOTLIB EXPORTS (old fig01/fig02 etc.)
         ========================= */
      if (d.type === "matplotlib_export") {
        const traces = [];
        (d.axes || []).forEach(ax => {
          (ax.lines || []).forEach(l => traces.push({ x: l.x, y: l.y, name: l.label || "", type: "scatter", mode: "lines" }));
          (ax.scatters || []).forEach(s => traces.push({ x: s.x, y: s.y, name: s.label || "", type: "scatter", mode: "markers" }));
          (ax.bars || []).forEach(b => traces.push({ x: [b.x], y: [b.height], type: "bar", name: "" }));
          (ax.polygons || []).forEach(pg => (pg.polys || []).forEach(p =>
            traces.push({ x: p.x, y: p.y, type: "scatter", mode: "lines", fill: "toself", name: pg.label || "" })
          ));
        });
        Plotly.newPlot(divId, traces, {
          title: d.axes?.[0]?.title || "",
          xaxis: { title: d.axes?.[0]?.xlabel || "" },
          yaxis: { title: d.axes?.[0]?.ylabel || "" }
        }, { responsive: true });
        return;
      }

      // Fallback: don’t silently draw garbage
      Plotly.newPlot(divId, [], {
        title: "Unsupported JSON",
        annotations: [{ text: `type=${d.type}, kind=${d.kind}`, showarrow: false }]
      }, { responsive: true });

    })
    .catch(err => {
      Plotly.newPlot(divId, [], { title: "Error loading JSON", annotations: [{ text: String(err), showarrow: false }] }, { responsive: true });
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

<div id="fig01" style="width:100%; height:500px;"></div>
<script>
fetch("{{ site.baseurl }}/assets/fig_json/fig01.json")
  .then(r => r.json())
  .then(fig => {
    Plotly.newPlot("fig01", fig.data, fig.layout, { responsive: true });
  });
</script>

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
