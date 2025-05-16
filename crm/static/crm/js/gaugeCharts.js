function getBarColor(score) {
    if (score >= 90) return "#50FF73";   // Green
    if (score >= 50) return "#FFDB28";   // Yellow
    return "#FF5028";                    // Red
}

function getBgColor(score) {
    if (score >= 90) return "#DDFFE4";   // Green
    if (score >= 50) return "#FFFBDD";   // Yellow
    return "#FFD0C6";                    // Red
}


function drawGaugePlot(elementId, score) {
    const data = [
        {
            type: "indicator",
            mode: "gauge+number",
            value: score,
            gauge: {
                axis: {
                    range: [0, 100],
                    showticklabels: false,
                    ticks: '',
                    tickwidth: 0,
                    tickcolor: "transparent"
                },
                bar: {
                    color: getBarColor(score),
                    thickness: 1
                },
                bgcolor: getBgColor(score),
                borderwidth: 0,
                bordercolor: "none",
                steps: [
                    { range: [0, 100], color: getBgColor(score) }
                ]
            }
        }
    ];

    const layout = {
        autosize: true,
        margin: { b: 0, t: 0, l: 0, r: 0, pad: 0},
        height: 200
    };

    Plotly.newPlot(elementId, data, layout);
}

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".score-gauge").forEach(function (el) {
        const score = parseFloat(el.dataset.score);
        if (!isNaN(score)) {
            drawGaugePlot(el.id, score);
        }
    });
});