<<<<<<< HEAD
const step = 0.005;
=======
const step = 0.0008;

>>>>>>> e5ba943 (Major UI update.)
let bgX = 0;
let bgY = 0;
let X = 0;
let Y = 0;

<<<<<<< HEAD
=======
const holdSpriteCount = 7;

>>>>>>> e5ba943 (Major UI update.)
const lengths = [5, 15];
const head_r = 6;
const bag = { 'w': 10, 'h': 10, 'r': 4 }
const normal_radius = 2;

<<<<<<< HEAD
let bg = document.getElementById("background-div");

const lerp = (start, end, t) => {
    return start + (end - start) * t;
=======
const mnColor = "#c0c0c0";
const secColor = "#0c0c0c";

const maxWidth = window.innerWidth;
let maxHeight = 0;
let maxHeightReady = false;

const sleep = ms => new Promise(r => setTimeout(r, ms));

function getMaxHeight() {
    return new Promise((resolve) => {
        requestAnimationFrame(() => {
            const body = document.body;
            const html = document.documentElement;
            maxHeight = Math.max(
                body.scrollHeight, body.offsetHeight, 
                html.clientHeight, html.scrollHeight, html.offsetHeight
              );
            resolve(maxHeight);
        });
    });
}

// Hacky checking to get the correct
// background height
document.addEventListener("DOMContentLoaded", () => {
    document.fonts.ready.then(() => {
    if (document.readyState === "complete") {
        getMaxHeight();
    } else {
        window.addEventListener("load", getMaxHeight());
    }
    });
});

let bg = document.getElementById("background-div");

const lerp = (start, end, t) => {
    var r = start + (end - start) * t;
    return r;
>>>>>>> e5ba943 (Major UI update.)
};

function isTouchDevice() {
    try {
        document.createEvent("TouchEvent");
        return true;

    } catch (e) {
        return false;

    }
}

const move = (e) => {
    try {
<<<<<<< HEAD
        var x = !isTouchDevice() ? e.pageX : e.touches[0].pageX;
        var y = !isTouchDevice() ? e.pageY : e.touches[0].pageY;

    } catch (e) {}
=======
        var x;
        var y;

        if (!isTouchDevice()) {
            x = e.pageX;
            y = e.pageY;

        } else {
            var touch = e.touches[0];
            x = touch.pageX;
            y = touch.pageY;

        }

    } catch (e) {
        console.error(`[Climber Background] Move error: ${e}`);
    }
>>>>>>> e5ba943 (Major UI update.)

    if (!(bg.style.left || bg.style.top)) {
        bg.style.left = x - 50 + "px";
        bg.style.top = y - 50 + "px";

        bgX = x - 50;
        bgY = y - 50;

    } else {
        bgX = x;
        bgY = y;
    }
};

function updatePos() {
    let left = Number(bg.style.left.substring(0, bg.style.left.length - 2));
    let top = Number(bg.style.top.substring(0, bg.style.top.length - 2));

    let newLeft = lerp(left, bgX, step);
    let newTop = lerp(top, bgY, step);

    bg.style.left = newLeft + "px";
    bg.style.top = newTop + "px";

    X = newLeft;
    Y = newTop;

    requestAnimationFrame(updatePos);
}

requestAnimationFrame(updatePos);

<<<<<<< HEAD
document.addEventListener("mousemove", (e) => {
    move(e);

});
document.addEventListener("touchmove", (e) => {
    move(e);

});
=======
if (!isTouchDevice()) {
    document.addEventListener("mousemove", (e) => {
        move(e);

    });

} else {
    document.addEventListener("touchmove", (e) => {
        move(e);

    });

}
>>>>>>> e5ba943 (Major UI update.)

function getTopPoint(x1, x2, y1, y2, a, o) {
    const c = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
    const h = Math.sqrt(Math.abs(Math.pow(a, 2) - Math.pow(c / 2, 2)));

    const xS = (x1 + x2) / 2;
    const yS = (y1 + y2) / 2;

    const xC = xS;
    const yC = yS + h * o;

    return [xC, yC];
}

<<<<<<< HEAD
function drawDot(context, x, y, r, color = 'black') {
=======
function drawDot(context, x, y, r, color = mnColor) {
>>>>>>> e5ba943 (Major UI update.)
    context.beginPath();
    context.arc(x, y, r, 0, Math.PI * 2, true);
    context.fillStyle = color;
    context.fill();
}

<<<<<<< HEAD
function drawCircle(context, x, y, r, color = 'black') {
=======
function drawCircle(context, x, y, r, color = mnColor) {
>>>>>>> e5ba943 (Major UI update.)
    context.beginPath();
    context.arc(x, y, r, 0, Math.PI * 2, true);
    context.strokeStyle = color;
    context.stroke();
}

var climber = {
    top_offset: { x: 0, y: -25 / 2 },
    bottom_offset: { x: 0, y: 25 / 2 }
};

function drawClimber(ctx, holds, lengths, canvas) {
<<<<<<< HEAD
    const normal_stroke = "gray";
=======
    const normal_stroke = mnColor;
>>>>>>> e5ba943 (Major UI update.)
    const normal_line_width = "1.2";
    const maxReach = 100;

    const canvas_center_x = X + canvas.width / 2;
    const canvas_center_y = Y + canvas.height / 2;

    const top_point = {
        x: canvas_center_x + climber.top_offset.x,
        y: canvas_center_y + climber.top_offset.y
    };
    const bottom_point = {
        x: canvas_center_x + climber.bottom_offset.x,
        y: canvas_center_y + climber.bottom_offset.y
    };

    const localize = (p) => ({ x: p.x - X, y: p.y - Y });

    function findClosestHold(holds, center, xSign, ySign) {
        return holds
            .filter(h => 
                (xSign === 0 || (xSign > 0 ? h.x >= center.x : h.x <= center.x)) &&
                (ySign === 0 || (ySign > 0 ? h.y >= center.y : h.y <= center.y)) &&
                distance(h, center) <= maxReach
            )
            .reduce((minEl, currentEl) => {
                return distance(currentEl, center) < distance(minEl, center) ? currentEl : minEl;
            }, holds[0]);
    }

    const limbs = [
        { center: top_point, xSign: 1, ySign: -1 },
        { center: top_point, xSign: -1, ySign: -1 },
        { center: bottom_point, xSign: -1, ySign: 1 },
        { center: bottom_point, xSign: 1, ySign: 1 }
    ];

    for (let i = 0; i < limbs.length; i++) {
        const { center, xSign, ySign } = limbs[i];
        var closest = findClosestHold(holds, center, xSign, ySign);

        if (!closest) continue;

        ctx.beginPath();
        ctx.strokeStyle = normal_stroke;
        ctx.lineWidth = normal_line_width;

        ctx.moveTo(localize(center).x, localize(center).y);
        ctx.lineTo(localize(closest).x, localize(closest).y);
        ctx.stroke();

        drawDot(ctx, localize(closest).x, localize(closest).y, normal_radius);
    }

    ctx.beginPath();
    ctx.strokeStyle = normal_stroke;
    ctx.lineWidth = normal_line_width;
    ctx.moveTo(localize(top_point).x, localize(top_point).y);
    ctx.lineTo(localize(bottom_point).x, localize(bottom_point).y);
    ctx.stroke();

    drawDot(ctx, localize(top_point).x, localize(top_point).y, normal_radius);
    drawDot(ctx, localize(bottom_point).x, localize(bottom_point).y, normal_radius);

<<<<<<< HEAD
    drawDot(ctx, localize(top_point).x, localize(top_point).y - head_r, head_r, "white");
=======
    drawDot(ctx, localize(top_point).x, localize(top_point).y - head_r, head_r, secColor);
>>>>>>> e5ba943 (Major UI update.)
    drawCircle(ctx, localize(top_point).x, localize(top_point).y - head_r, head_r, normal_stroke);
}

function stringToSeed(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i);
        hash = (hash * 31 + char) | 0;
    }
  
    return Math.abs(hash);
}

function mulberry32(seed) {
    return function() {
        let t = seed += 0x6D2B79F5;
        t = Math.imul(t ^ (t >>> 15), t | 1);
        t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
        return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    }
}

// config for the holds
const config = {
    minDistance: 40,
    seed: stringToSeed('Lenart Kladnik')
};

function getRandomFloat(min, max, rng) {
    return rng() * (max - min) + min;
}

function getRandomInt(min, max, rng) {
    return Math.floor(getRandomFloat(min, max, rng));
}

function distance(p1, p2) {
    const dx = p1.x - p2.x;
    const dy = p1.y - p2.y;
    return Math.sqrt(dx * dx + dy * dy);
}

function getHolds(width, height) {
    const { minDistance, seed } = config;
    const rng = mulberry32(seed);
    const holds = [];

    let attempts = 0;
    const maxAttempts = 10000; // safety to avoid infinite loops

    while (attempts < maxAttempts) {
        const point = {
            x: getRandomFloat(0, width, rng),
            y: getRandomFloat(0, height, rng)
        };

        const tooClose = holds.some(existing => distance(existing, point) < minDistance);

        if (!tooClose) {
            holds.push(point);
        }

        attempts++;
    }

    return holds;
}

<<<<<<< HEAD
const holds_svgs = [];

for (let i = 0; i < 7; i++) {
    const svgUrl = `/static/hold_${i}.svg`;

    fetch(svgUrl)
        .then(response => response.text())
        .then(svgText => {
            const blob = new Blob([svgText], { type: 'image/svg+xml' });
            const url = URL.createObjectURL(blob);

            const img = new Image();
            img.onload = () => {
                holds_svgs[i] = img;
                URL.revokeObjectURL(url);
            };
            img.src = url;
        })
        .catch(err => {
            console.error(`Failed to load SVG ${i}:`, err);
            holds_svgs[i] = null;
        });
}

function drawHold(ctx, x, y, canvas, holds_index, gray) {
    const w = 10;
    const h = 10;

    let hold = getRandomInt(0, 7, mulberry32(holds_index));

    const img = holds_svgs[hold];
    if (img) {
        if (gray) { ctx.filter = 'brightness(300%) contrast(5%)'; }
=======
function loadHolds() {
    const holds = [];

    for (let i = 0; i < holdSpriteCount; i++) {
        const svgUrl = `/static/hold_${i}.svg`;

        fetch(svgUrl)
            .then(response => response.text())
            .then(svgText => {
                const blob = new Blob([svgText], { type: 'image/svg+xml' });
                const url = URL.createObjectURL(blob);

                const img = new Image();
                img.onload = () => {
                    holds[i] = img;
                    URL.revokeObjectURL(url);
                };
                img.src = url;

            console.log(`[Climber Background] Loaded hold SVG ${i}.`);
        })
        .catch(e => {
            console.error(`[Climber Background] Failed to load hold SVG ${i}: ${e}`);
            holds[i] = null;
        });
    }

    return holds;
}

var holds_svgs = loadHolds();

function drawHold(ctx, x, y, canvas, holds_index, highlight) {
    if (holds_svgs.length !== holdSpriteCount) {
        console.warn(`[Climber Background] Attempted draw when holds aren't loaded yet!`);

        return 1;
    }

    const w = 10;
    const h = 10;

    const hold = getRandomInt(0, holdSpriteCount, mulberry32(holds_index));

    const img = holds_svgs[hold];
    try {
        if (highlight) { ctx.filter = 'brightness(100%) contrast(0%)'; }
        else { ctx.filter = 'brightness(50%) contrast(20%)'; }

>>>>>>> e5ba943 (Major UI update.)
        ctx.drawImage(img, x, y, w, h);
        ctx.filter = 'none';

        return 0;

<<<<<<< HEAD
    } else {
=======
    } catch (e) {
        console.error(`[Climber Background] Failed to draw hold ${hold} (${img}) with holds=(${holds_svgs}): ${e}.`);

>>>>>>> e5ba943 (Major UI update.)
        return 1;
    }
}

<<<<<<< HEAD
function drawHolds(context, holds, x_s, y_s, x_e, y_e, canvas, gray=false) {
=======
function drawHolds(context, holds, x_s, y_s, x_e, y_e, canvas, highlight) {
>>>>>>> e5ba943 (Major UI update.)
    const displayed = [];

    for (var i = 0; i < holds.length; i++) {
        x = holds[i].x;
        y = holds[i].y;

        if (x_s <= x && x <= x_e && y_s <= y && y <= y_e) {
<<<<<<< HEAD
            r = drawHold(context, x - x_s, y - y_s, canvas, i, gray);
=======
            r = drawHold(context, x - x_s, y - y_s, canvas, i, highlight);
>>>>>>> e5ba943 (Major UI update.)

            displayed.push(holds[i]);
        }
    }

    return [displayed, r];
}

const fadeMargin = 50;

function applyFading(ctx, canvas) {
    const maxRadius = Math.sqrt(Math.pow(canvas.width / 2 + fadeMargin, 2) + Math.pow(canvas.height / 2 + fadeMargin, 2));

    ctx.globalCompositeOperation = 'destination-in';

    const gradient = ctx.createRadialGradient(
      canvas.width / 2, canvas.height / 2, 0,
      canvas.width / 2, canvas.height / 2, maxRadius
    );

    gradient.addColorStop(0.0, 'rgba(0, 0, 0, 1)');
    gradient.addColorStop(canvas.width / 2 / maxRadius, 'rgba(0, 0, 0, 1)');
    gradient.addColorStop(1.0, 'rgba(0, 0, 0, 0)');

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.globalCompositeOperation = 'source-over';
}

<<<<<<< HEAD
const holds = getHolds(document.documentElement.scrollWidth, window.screen.height);

function drawBgClimber() {
=======
function maxHeightCheck() {
    if (!maxHeightReady) {
        console.warn('[Climber Background] Error maxHeight is not ready yet!');
        getMaxHeight();

        sleep(200);

        return false;
    }

    console.debug(maxHeight);

    return true;
}

let holds = getHolds(maxWidth, maxHeight);

function drawBgClimber() {
    maxHeightCheck();

>>>>>>> e5ba943 (Major UI update.)
    var canvas = document.getElementById('climber');
    var ctx = canvas.getContext("2d");

    ctx.clearRect(0, 0, canvas.width, canvas.height);

<<<<<<< HEAD
    var [displayed_holds, _] = drawHolds(ctx, holds, X, Y, X + canvas.width, Y + canvas.height, canvas);
=======
    var [displayed_holds, _] = drawHolds(ctx, holds, X, Y, X + canvas.width, Y + canvas.height, canvas, true);
>>>>>>> e5ba943 (Major UI update.)
    drawClimber(ctx, holds, lengths, canvas);

    applyFading(ctx, canvas);

    requestAnimationFrame(drawBgClimber);
}

function drawBgHolds() {
<<<<<<< HEAD
    var canvas = document.getElementById('holds');
    var ctx = canvas.getContext("2d");

    canvas.width = document.documentElement.scrollWidth;
    canvas.height = window.screen.height;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    var [_, r] = drawHolds(ctx, holds, 0, 0, canvas.width, canvas.height, canvas, true);

    if (r == 1) {
=======
    res = maxHeightCheck();

    holds = getHolds(maxWidth, maxHeight);

    var canvas = document.getElementById('holds');
    var ctx = canvas.getContext("2d");

    canvas.width = maxWidth;
    canvas.height = maxHeight;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    var [_, r] = drawHolds(ctx, holds, 0, 0, canvas.width, canvas.height, canvas, false);

    if (r === 1 || !res) {
>>>>>>> e5ba943 (Major UI update.)
        requestAnimationFrame(drawBgHolds);
    }
}

requestAnimationFrame(drawBgClimber);
requestAnimationFrame(drawBgHolds);

function toggleNextSibling(event) {
    var toggle = event.currentTarget;
    toggle.textContent = toggle.textContent == '>' ? '/': '>';
    var nextSibling = toggle.nextSibling;
    while(nextSibling && nextSibling.nodeType != 1) {
        nextSibling = nextSibling.nextSibling;
    }

    nextSibling.classList.toggle('show');
}
<<<<<<< HEAD

// toggles = document.getElementsByClassName('toggle');
// for (var i = 0; i < toggles.length; i++) {
//     var toggle = toggles[i];
//     toggle.addEventListener('click', toggleNextSibling);
// }
=======
>>>>>>> e5ba943 (Major UI update.)
