const chart = document.querySelector("#bubble-chart");
const tooltip = document.querySelector("#tooltip");
const tableBody = document.querySelector("#score-table");
const showObservation = document.querySelector("#show-observation");
const layerFilter = document.querySelector("#layer-filter");
const confidenceFilter = document.querySelector("#confidence-filter");
const confidenceOutput = document.querySelector("#confidence-output");
const exportButton = document.querySelector("#export-button");

const colors = { "上游": "#d96b43", "中游": "#4f8bd6", "下游": "#45a579" };
let sectors = [];
let filteredSectors = [];

function svgElement(tag, attributes = {}) {
  const element = document.createElementNS("http://www.w3.org/2000/svg", tag);
  Object.entries(attributes).forEach(([key, value]) => element.setAttribute(key, value));
  return element;
}

function renderAxes() {
  const left = 85, right = 1050, top = 35, bottom = 585;
  for (let score = 0; score <= 100; score += 20) {
    const x = left + (score / 100) * (right - left);
    const y = bottom - (score / 100) * (bottom - top);
    chart.append(svgElement("line", { x1: x, y1: top, x2: x, y2: bottom, class: "grid-line" }));
    chart.append(svgElement("line", { x1: left, y1: y, x2: right, y2: y, class: "grid-line" }));
    const xText = svgElement("text", { x, y: bottom + 23, class: "axis-label", "text-anchor": "middle" });
    xText.textContent = score;
    chart.append(xText);
    const yText = svgElement("text", { x: left - 15, y: y + 4, class: "axis-label", "text-anchor": "end" });
    yText.textContent = score;
    chart.append(yText);
  }
  chart.append(svgElement("line", { x1: left, y1: bottom, x2: right, y2: bottom, class: "axis-line" }));
  chart.append(svgElement("line", { x1: left, y1: top, x2: left, y2: bottom, class: "axis-line" }));
  const xLabel = svgElement("text", { x: (left + right) / 2, y: 635, class: "axis-label", "text-anchor": "middle" });
  xLabel.textContent = "围墙分：低 → 高";
  chart.append(xLabel);
  const yLabel = svgElement("text", { x: 24, y: (top + bottom) / 2, class: "axis-label", transform: `rotate(-90 24 ${(top + bottom) / 2})`, "text-anchor": "middle" });
  yLabel.textContent = "利润分：低 → 高";
  chart.append(yLabel);
}

function tooltipHtml(item) {
  return `<strong>${item.name}</strong><br>
    增长分：${item.growth.toFixed(1)}<br>
    利润分：${item.profit.toFixed(1)}<br>
    围墙分：${item.moat.toFixed(1)}<br>
    产业质量分：${item.quality.toFixed(1)}<br>
    估值温度：${item.valuation.toFixed(1)}<br>
    市场状态：${item.market.toFixed(1)}<br>
    数据置信度：${item.confidence.toFixed(1)}<br>
    研究状态：${item.status}`;
}

function renderChart(items) {
  chart.replaceChildren();
  renderAxes();
  const left = 85, right = 1050, top = 35, bottom = 585;
  items.forEach((item) => {
    const x = left + (item.moat / 100) * (right - left);
    const y = bottom - (item.profit / 100) * (bottom - top);
    const radius = 12 + item.growth * 0.27;
    const circle = svgElement("circle", {
      cx: x, cy: y, r: radius, fill: colors[item.layer], opacity: item.ranked ? 0.72 : 0.48,
      stroke: item.ranked ? "#ffffff" : "#345e52", "stroke-width": item.ranked ? 1.5 : 2.5,
      class: "bubble", tabindex: 0,
    });
    const showTip = (event) => {
      tooltip.innerHTML = tooltipHtml(item);
      tooltip.hidden = false;
      const bounds = document.querySelector(".chart-wrap").getBoundingClientRect();
      tooltip.style.left = `${Math.min(event.clientX - bounds.left + 14, bounds.width - 245)}px`;
      tooltip.style.top = `${Math.max(event.clientY - bounds.top - 40, 8)}px`;
    };
    circle.addEventListener("mousemove", showTip);
    circle.addEventListener("mouseenter", showTip);
    circle.addEventListener("mouseleave", () => { tooltip.hidden = true; });
    chart.append(circle);
    const label = svgElement("text", { x, y: y - radius - 6, class: "bubble-label" });
    label.textContent = item.name;
    chart.append(label);
  });
}

function renderTable(items) {
  tableBody.replaceChildren();
  [...items].sort((a, b) => b.quality - a.quality).forEach((item) => {
    const row = document.createElement("tr");
    [item.name, item.layer, item.growth, item.profit, item.moat, item.quality,
      item.valuation, item.market, item.confidence, item.status].forEach((value) => {
      const cell = document.createElement("td");
      cell.textContent = typeof value === "number" ? value.toFixed(1) : value;
      row.append(cell);
    });
    tableBody.append(row);
  });
}

function applyFilters() {
  const layer = layerFilter.value;
  const minimumConfidence = Number(confidenceFilter.value);
  confidenceOutput.value = minimumConfidence;
  filteredSectors = sectors.filter((item) => {
    if (!showObservation.checked && !item.ranked) return false;
    if (layer !== "全部" && item.layer !== layer) return false;
    return item.confidence >= minimumConfidence;
  });
  renderChart(filteredSectors);
  renderTable(filteredSectors);
}

function updateSummary() {
  const ranked = sectors.filter((item) => item.ranked);
  const highest = [...ranked].sort((a, b) => b.quality - a.quality)[0];
  document.querySelector("#ranked-count").textContent = ranked.length;
  document.querySelector("#observation-count").textContent = sectors.length - ranked.length;
  document.querySelector("#research-count").textContent = ranked.filter((item) => item.status === "重点研究").length;
  document.querySelector("#top-quality").textContent = highest.quality.toFixed(1);
}

function exportCsv() {
  const headers = ["板块", "层级", "增长分", "利润分", "围墙分", "产业质量分", "估值温度", "市场状态", "置信度", "研究状态", "数据日期"];
  const rows = filteredSectors.map((item) => [item.name, item.layer, item.growth, item.profit, item.moat,
    item.quality, item.valuation, item.market, item.confidence, item.status, item.as_of_date]);
  const quote = (value) => `"${String(value).replaceAll('"', '""')}"`;
  const csv = [headers, ...rows].map((row) => row.map(quote).join(",")).join("\r\n");
  const link = document.createElement("a");
  link.href = URL.createObjectURL(new Blob(["\ufeff", csv], { type: "text/csv;charset=utf-8" }));
  link.download = "three-high-sector-demo.csv";
  link.click();
  URL.revokeObjectURL(link.href);
}

[showObservation, layerFilter, confidenceFilter].forEach((control) => control.addEventListener("input", applyFilters));
exportButton.addEventListener("click", exportCsv);

fetch("/api/sectors")
  .then((response) => {
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  })
  .then((payload) => {
    sectors = payload.sectors;
    document.querySelector("#version").textContent = `模型 ${payload.metadata.model_version}`;
    document.querySelector("#notice").textContent = payload.metadata.disclaimer;
    updateSummary();
    applyFilters();
  })
  .catch((error) => {
    document.querySelector("#notice").textContent = `数据加载失败：${error.message}`;
  });
