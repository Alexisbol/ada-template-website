---
layout: default
layout: default
title: Fed Rate Impact Game
permalink: /game/
Pick a sector, company size, and Fed rate event. Hit **Reveal** to see which profile is expected to perform better and why.
# Fed Rate Impact Game

Pick a sector, company size, and Fed rate event. Hit **Reveal** to see which profile is expected to perform better and why.

<div class="game-hero">
	<div class="game-hero__content">
		<p class="eyebrow">Macro matchup</p>
		<h2>Which profile wins this Fed move?</h2>
		<p class="subhead">Adjust the dials and see how sectors and company sizes react when policy shifts.</p>
	</div>
	<div class="game-hero__badge">FFR focus</div>
</div>

<div class="game-card">
	<div class="game-grid">
		<label class="game-field">
			<span>Sector</span>
			<select id="sector">
				<option value="Technology">Technology</option>
				<option value="Utilities">Utilities</option>
			</select>
		</label>

		<label class="game-field">
			<span>Company Size</span>
			<select id="size">
				<option value="Large">Large Cap</option>
				<option value="Small">Small Cap</option>
			</select>
		</label>

		<label class="game-field">
			<span>Fed Event</span>
			<select id="event">
				<option value="Hike">Rate Hike</option>
				<option value="Cut">Rate Cut</option>
				<option value="Hold">No Change / Hold</option>
			</select>
		</label>
	</div>

	<button id="reveal" class="game-btn">Reveal outcome</button>

	<div id="result" class="game-result" aria-live="polite"></div>

	<ul class="game-notes">
		<li>Tech = higher duration; Utilities = defensive/bond-proxy.</li>
		<li>Small caps feel funding costs more than large caps.</li>
		<li>Hikes pressure valuations; cuts ease financing and boost risk-on assets.</li>
	</ul>
</div>

<script>
	(function() {
		const outcomes = {
			"Technology-Large-Hike": {
				performance: "Likely lags Utilities Large Cap",
				why: "Long-duration cash flows get discounted harder when rates rise; large caps cushion with cash but growth rerates lower."
			},
			"Technology-Small-Hike": {
				performance: "Likely underperforms all peers",
				why: "Financing costs spike and valuations compress fastest for small, growthy names."
			},
			"Utilities-Large-Hike": {
				performance: "Defensive, but pressured vs Utilities Small Cap",
				why: "Bond-proxy traits hurt when yields rise, yet scale and regulated revenue soften the blow."
			},
			"Utilities-Small-Hike": {
				performance: "Slightly better than Tech but still constrained",
				why: "Lower duration than tech helps, but higher debt loads make small utilities rate-sensitive."
			},
			"Technology-Large-Cut": {
				performance: "Often leads",
				why: "Lower discount rates boost long-duration growth; strong balance sheets capture the upside."
			},
			"Technology-Small-Cut": {
				performance: "High beta winner",
				why: "Cheap capital fuels expansion and re-rating, giving small growth outsized upside."
			},
			"Utilities-Large-Cut": {
				performance: "Stable but trails Tech",
				why: "Income profile benefits from lower yields, yet growthier sectors typically outpace."
			},
			"Utilities-Small-Cut": {
				performance: "Modest upside",
				why: "Borrowing gets cheaper, but limited growth keeps gains muted versus tech."
			},
			"Technology-Large-Hold": {
				performance: "Tracks fundamentals",
				why: "With policy steady, earnings delivery and guidance drive returns."
			},
			"Technology-Small-Hold": {
				performance: "Choppy, story-driven",
				why: "Steady rates remove a tailwind; stock picking matters more than macro."
			},
			"Utilities-Large-Hold": {
				performance: "Range-bound defensive",
				why: "Yield support is stable; movement comes from regulation and fuel costs."
			},
			"Utilities-Small-Hold": {
				performance: "Low-beta, modest moves",
				why: "Less rate noise; local fundamentals dominate."
			}
		};

		const sectorEl = document.getElementById("sector");
		const sizeEl = document.getElementById("size");
		const eventEl = document.getElementById("event");
		const resultEl = document.getElementById("result");
		const btn = document.getElementById("reveal");

		btn.addEventListener("click", function() {
			const key = `${sectorEl.value}-${sizeEl.value}-${eventEl.value}`;
			const outcome = outcomes[key];
			if (!outcome) return;
			resultEl.classList.add("show");
			resultEl.innerHTML = `<span class="pill">Outcome</span> ${outcome.performance}<br><span class="pill pill-muted">Why</span> ${outcome.why}`;
		});
	})();
</script>
