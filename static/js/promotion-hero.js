// Promotion hero (core/hero-promotion.html): endless gold confetti.
document.addEventListener('DOMContentLoaded', function () {
    const hero = document.getElementById('promoHero');
    if (!hero) return;
    const canvas = hero.querySelector('.promo-confetti');
    if (!canvas || !canvas.getContext) return;
    const ctx = canvas.getContext('2d');

    // Club gold in a few shades, plus a little white, so the confetti looks metallic
    const COLORS = ['#b6a265', '#cbb878', '#e6d8a8', '#9c8850', '#f3ead0', '#ffffff'];
    const SHINE = '#fff6d6';
    const PIECES_PER_PIXEL = 1 / 8500;  // density: about 150 pieces on a 1440x900 screen
    const MIN_PIECES = 45;
    const MAX_PIECES = 170;
    const BURST_PIECES = 70;            // per side, fired once when the page opens
    const MAX_PIXEL_RATIO = 2;          // sharper than that costs battery without looking better
    const MAX_FRAME_GAP = 50;           // ms; after a pause, pieces continue instead of jumping

    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    let width = 0;
    let height = 0;
    let pieces = [];
    let running = false;
    let onScreen = true;
    let lastTime = 0;

    function random(min, max) {
        return min + Math.random() * (max - min);
    }

    // ------------------------------------------------------------
    // Pieces – "rain" falls forever and starts over at the top;
    // "burst" pieces shoot up from the corners once and then fade away
    // ------------------------------------------------------------
    function makePiece(burst) {
        const depth = random(0.55, 1.15);  // smaller and slower pieces read as further away
        const roll = Math.random();
        return {
            x: random(0, width),
            y: random(-height, 0),
            depth: depth,
            shape: roll < 0.6 ? 'rect' : roll < 0.85 ? 'dot' : 'ribbon',
            w: random(6, 11) * depth,
            h: random(9, 16) * depth,
            color: COLORS[Math.floor(Math.random() * COLORS.length)],
            vx: random(-0.25, 0.25),
            vy: random(0.7, 1.5) * depth,
            sway: random(0, Math.PI * 2),
            swaySpeed: random(0.01, 0.03),
            swayWidth: random(8, 26) * depth,
            rotation: random(0, Math.PI * 2),
            spin: random(-0.04, 0.04),
            flip: random(0, Math.PI * 2),
            flipSpeed: random(0.04, 0.1),
            burst: burst
        };
    }

    function makeBurstPiece(fromLeft) {
        const piece = makePiece(true);
        const angle = fromLeft ? random(-1.25, -0.75) : random(-2.4, -1.9);  // up and inwards
        const speed = random(9, 17);
        piece.x = fromLeft ? random(-10, 20) : random(width - 20, width + 10);
        piece.y = height + 10;
        piece.vx = Math.cos(angle) * speed;
        piece.vy = Math.sin(angle) * speed;
        return piece;
    }

    function targetCount() {
        return Math.round(Math.min(MAX_PIECES, Math.max(MIN_PIECES, width * height * PIECES_PER_PIXEL)));
    }

    // Keep the right number of falling pieces after a resize; burst pieces are left alone
    function fillRain(spreadOverScreen) {
        const rain = pieces.filter(function (p) { return !p.burst; });
        const missing = targetCount() - rain.length;
        if (missing < 0) {
            let extra = -missing;
            pieces = pieces.filter(function (p) {
                if (!p.burst && extra > 0) { extra--; return false; }
                return true;
            });
            return;
        }
        for (let i = 0; i < missing; i++) {
            const piece = makePiece(false);
            if (spreadOverScreen) piece.y = random(-20, height);
            pieces.push(piece);
        }
    }

    // ------------------------------------------------------------
    // Drawing
    // ------------------------------------------------------------
    function resize() {
        const ratio = Math.min(window.devicePixelRatio || 1, MAX_PIXEL_RATIO);
        width = hero.clientWidth;
        height = hero.clientHeight;
        canvas.width = Math.round(width * ratio);
        canvas.height = Math.round(height * ratio);
        ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    }

    function drawPiece(p) {
        // cos(flip) squashes the piece as if it turns in the air; facing us, it catches the light
        const facing = Math.cos(p.flip);
        ctx.save();
        ctx.translate(p.x + Math.sin(p.sway) * p.swayWidth, p.y);
        ctx.rotate(p.rotation);
        ctx.globalAlpha = (p.burst ? Math.min(1, p.life) : 1) * (0.55 + 0.45 * p.depth);
        ctx.fillStyle = facing > 0.85 ? SHINE : p.color;
        ctx.strokeStyle = ctx.fillStyle;

        if (p.shape === 'dot') {
            ctx.beginPath();
            ctx.ellipse(0, 0, p.w * 0.45, p.w * 0.45 * Math.abs(facing) + 0.6, 0, 0, Math.PI * 2);
            ctx.fill();
        } else if (p.shape === 'ribbon') {
            ctx.lineWidth = 2 * p.depth;
            ctx.beginPath();
            ctx.moveTo(-p.h, 0);
            ctx.quadraticCurveTo(0, p.h * facing, p.h, 0);
            ctx.stroke();
        } else {
            ctx.scale(1, facing);
            ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h);
        }
        ctx.restore();
    }

    function step(p, speed) {
        p.sway += p.swaySpeed * speed;
        p.rotation += p.spin * speed;
        p.flip += p.flipSpeed * speed;

        if (p.burst) {
            // Thrown pieces slow down in the air and settle into a gentle fall
            p.vx *= Math.pow(0.97, speed);
            p.vy = p.vy * Math.pow(0.97, speed) + 0.18 * speed;
            p.vy = Math.min(p.vy, 2.2 * p.depth);
            p.life = p.life === undefined ? 4 : p.life - 0.004 * speed;
        }
        p.x += p.vx * speed;
        p.y += p.vy * speed;

        // A rain piece that leaves the hero starts over at the top: the confetti never runs out
        if (!p.burst && p.y > height + 20) {
            p.y = random(-40, -10);
            p.x = random(0, width);
        }
        if (!p.burst && p.x < -40) p.x = width + 30;
        if (!p.burst && p.x > width + 40) p.x = -30;
    }

    function frame(now) {
        if (!running) return;
        const gap = lastTime ? Math.min(now - lastTime, MAX_FRAME_GAP) : 16.7;
        const speed = gap / 16.7;  // the same pace on 60 Hz and 120 Hz screens
        lastTime = now;

        ctx.clearRect(0, 0, width, height);
        pieces = pieces.filter(function (p) {
            return !p.burst || (p.life === undefined || p.life > 0) && p.y < height + 30;
        });
        pieces.forEach(function (p) {
            step(p, speed);
            drawPiece(p);
        });
        window.requestAnimationFrame(frame);
    }

    // ------------------------------------------------------------
    // Only animate while someone can see it – saves battery on phones
    // ------------------------------------------------------------
    function updateRunning() {
        const shouldRun = onScreen && !document.hidden;
        if (shouldRun === running) return;
        running = shouldRun;
        if (running) {
            lastTime = 0;
            window.requestAnimationFrame(frame);
        }
    }

    function drawStill() {
        ctx.clearRect(0, 0, width, height);
        pieces.forEach(drawPiece);
    }

    resize();
    fillRain(true);

    if (reduceMotion) {
        drawStill();
    } else {
        for (let i = 0; i < BURST_PIECES; i++) {
            pieces.push(makeBurstPiece(true));
            pieces.push(makeBurstPiece(false));
        }
        if ('IntersectionObserver' in window) {
            new IntersectionObserver(function (entries) {
                onScreen = entries[0].isIntersecting;
                updateRunning();
            }).observe(hero);
        }
        document.addEventListener('visibilitychange', updateRunning);
        updateRunning();
    }

    let resizeTimer;
    window.addEventListener('resize', function () {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function () {
            resize();
            fillRain(false);
            if (reduceMotion) drawStill();
        }, 150);
    });
});


// ------------------------------------------------------------
// Herrer / Kvinner carousel: the teams take turns, and each turn
// shows that team's next photo, so no photo comes twice in a row.
// The division line under OPPRYKK! follows the team. A click on a
// team jumps to it and the carousel carries on from there.
// ------------------------------------------------------------
document.addEventListener('DOMContentLoaded', function () {
    const hero = document.getElementById('promoHero');
    if (!hero) return;
    const buttons = hero.querySelectorAll('.promo-team');
    if (!buttons.length) return;

    const SLIDE_INTERVAL = 2000;  // ms; same as $slideInterval in promotion-hero.scss
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    const teams = Array.prototype.map.call(buttons, function (button) { return button.dataset.team; });
    const photos = {};
    const nextPhoto = {};
    teams.forEach(function (team) {
        photos[team] = hero.querySelectorAll('.promo-photo[data-team="' + team + '"]');
        nextPhoto[team] = 0;
    });

    let current = teams[0];
    nextPhoto[current] = 1;  // the first men's photo is already showing from the server
    let timer = null;

    function showTeam(team) {
        current = team;
        const list = photos[team];
        const photo = list.length ? list[nextPhoto[team] % list.length] : null;
        nextPhoto[team] += 1;

        hero.querySelectorAll('.promo-photo').forEach(function (el) {
            el.classList.toggle('is-active', el === photo);
        });
        hero.querySelectorAll('.division-line').forEach(function (el) {
            const active = el.dataset.team === team;
            el.classList.toggle('is-active', active);
            el.setAttribute('aria-hidden', active ? 'false' : 'true');
        });
        buttons.forEach(function (el) {
            const active = el.dataset.team === team;
            el.classList.toggle('is-active', active);
            el.setAttribute('aria-pressed', active ? 'true' : 'false');
        });
    }

    // Restarts the countdown and the progress line under the active team
    function play() {
        if (reduceMotion) return;
        clearTimeout(timer);
        hero.classList.remove('is-playing');
        void hero.offsetWidth;
        hero.classList.add('is-playing');
        timer = setTimeout(function () {
            showTeam(teams[(teams.indexOf(current) + 1) % teams.length]);
            play();
        }, SLIDE_INTERVAL);
    }

    buttons.forEach(function (button) {
        button.addEventListener('click', function () {
            showTeam(button.dataset.team);
            play();
        });
    });

    play();
});


// ------------------------------------------------------------
// "Send dine gratulasjoner": a full-screen popup with gold fireworks,
// the .cheer-word lines flying through one by one, then a thank-you card.
// Nothing is sent anywhere – it is a celebration for the visitor.
// ------------------------------------------------------------
document.addEventListener('DOMContentLoaded', function () {
    const openButton = document.getElementById('promoCheerOpen');
    const popup = document.getElementById('promoCheer');
    if (!openButton || !popup) return;
    const canvas = popup.querySelector('.cheer-fireworks');
    if (!canvas || !canvas.getContext) return;
    const ctx = canvas.getContext('2d');
    const words = popup.querySelectorAll('.cheer-word');
    const closeButtons = popup.querySelectorAll('[data-cheer-close]');

    const PALETTES = [
        ['#b6a265', '#e6d8a8', '#fff6d6'],   // club gold
        ['#cbb878', '#f3ead0', '#ffffff'],   // pale gold and white
        ['#9c8850', '#b6a265', '#f4e4ad'],   // deep gold
        ['#ffffff', '#e6d8a8', '#b6a265']    // white burst with gold tips
    ];
    const GRAVITY = 0.05;
    const ROCKET_GRAVITY = GRAVITY * 2.2;  // rockets slow down faster than sparks fall, so they burst high
    const DRAG = 0.982;
    const MIN_LAUNCH_GAP = 450;   // ms between rockets while the popup is open
    const MAX_LAUNCH_GAP = 900;
    const WORD_GAP = 1150;        // ms between flying words; each flies for 1.75 s, so they overlap a little
    const WORD_FLIGHT = 1750;     // ms, matches the cheerFly animation in promotion-hero.scss
    const MAX_PIXEL_RATIO = 2;
    const MAX_FRAME_GAP = 50;

    // Where each word flies in from, in turn: below, left, right, above...
    const DIRECTIONS = [
        ['0px', '220px', '-6deg'], ['-60vw', '40px', '-14deg'], ['60vw', '-40px', '12deg'],
        ['0px', '-220px', '6deg'], ['-40vw', '160px', '10deg'], ['40vw', '160px', '-10deg']
    ];

    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    let width = 0;
    let height = 0;
    let rockets = [];
    let sparks = [];
    let flashes = [];
    let running = false;
    let lastTime = 0;
    let timers = [];

    function random(min, max) {
        return min + Math.random() * (max - min);
    }

    function later(callback, delay) {
        timers.push(setTimeout(callback, delay));
    }

    function resize() {
        const ratio = Math.min(window.devicePixelRatio || 1, MAX_PIXEL_RATIO);
        width = popup.clientWidth;
        height = popup.clientHeight;
        canvas.width = Math.round(width * ratio);
        canvas.height = Math.round(height * ratio);
        ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    }

    // ------------------------------------------------------------
    // Fireworks – a rocket climbs until it stops rising, then bursts
    // ------------------------------------------------------------
    function launch() {
        const x = random(width * 0.12, width * 0.88);
        const targetY = random(height * 0.12, height * 0.45);
        rockets.push({
            x: x,
            y: height + 10,
            px: x,
            py: height + 10,
            vx: random(-0.8, 0.8),
            vy: -Math.sqrt(2 * ROCKET_GRAVITY * (height - targetY))  // just enough speed to reach targetY
        });
    }

    function explode(x, y) {
        const palette = PALETTES[Math.floor(Math.random() * PALETTES.length)];
        const count = Math.round(random(80, 120));
        // Smaller bursts on phones so they don't fill the whole screen
        const power = random(3.8, 6.8) * Math.min(1, Math.max(0.65, width / 1200));
        for (let i = 0; i < count; i++) {
            const angle = (i / count) * Math.PI * 2 + random(-0.08, 0.08);
            const speed = power * random(0.55, 1);
            sparks.push({
                x: x,
                y: y,
                px: x,
                py: y,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                life: 1,
                decay: random(0.009, 0.017),
                color: palette[Math.floor(Math.random() * palette.length)],
                glitter: Math.random() < 0.3
            });
        }
        flashes.push({ x: x, y: y, life: 1 });
    }

    function drawRockets(speed) {
        ctx.strokeStyle = 'rgba(246, 236, 200, .9)';
        ctx.lineWidth = 2.5;
        rockets = rockets.filter(function (r) {
            r.px = r.x;
            r.py = r.y;
            r.vy += ROCKET_GRAVITY * speed;
            r.x += r.vx * speed;
            r.y += r.vy * speed;
            ctx.beginPath();
            ctx.moveTo(r.px, r.py + 8);
            ctx.lineTo(r.x, r.y);
            ctx.stroke();
            if (r.vy >= 0) {
                explode(r.x, r.y);
                return false;
            }
            return true;
        });
    }

    function drawFlashes(speed) {
        flashes = flashes.filter(function (f) {
            const radius = 90 * (1.4 - f.life);
            const glow = ctx.createRadialGradient(f.x, f.y, 0, f.x, f.y, radius);
            glow.addColorStop(0, 'rgba(255, 244, 210, ' + 0.55 * f.life + ')');
            glow.addColorStop(1, 'rgba(182, 162, 101, 0)');
            ctx.fillStyle = glow;
            ctx.beginPath();
            ctx.arc(f.x, f.y, radius, 0, Math.PI * 2);
            ctx.fill();
            f.life -= 0.08 * speed;
            return f.life > 0;
        });
    }

    function drawSparks(speed) {
        sparks = sparks.filter(function (s) {
            s.px = s.x;
            s.py = s.y;
            s.vx *= Math.pow(DRAG, speed);
            s.vy = s.vy * Math.pow(DRAG, speed) + GRAVITY * speed;
            s.x += s.vx * speed;
            s.y += s.vy * speed;
            s.life -= s.decay * speed;
            if (s.life <= 0) return false;

            // Glitter sparks twinkle as they fade out
            const alpha = s.glitter && s.life < 0.55 ? s.life * random(0.2, 1.6) : s.life;
            ctx.globalAlpha = Math.max(0, Math.min(1, alpha));
            ctx.strokeStyle = s.color;
            ctx.lineWidth = 2.2 * s.life + 0.6;
            ctx.beginPath();
            ctx.moveTo(s.px, s.py);
            ctx.lineTo(s.x, s.y);
            ctx.stroke();
            return true;
        });
        ctx.globalAlpha = 1;
    }

    function frame(now) {
        if (!running) return;
        const gap = lastTime ? Math.min(now - lastTime, MAX_FRAME_GAP) : 16.7;
        const speed = gap / 16.7;  // the same pace on 60 Hz and 120 Hz screens
        lastTime = now;

        ctx.clearRect(0, 0, width, height);
        ctx.globalCompositeOperation = 'lighter';  // overlapping sparks glow brighter, like real fireworks
        ctx.lineCap = 'round';
        drawRockets(speed);
        drawFlashes(speed);
        drawSparks(speed);
        ctx.globalCompositeOperation = 'source-over';

        window.requestAnimationFrame(frame);
    }

    function keepLaunching() {
        launch();
        later(keepLaunching, random(MIN_LAUNCH_GAP, MAX_LAUNCH_GAP));
    }

    // ------------------------------------------------------------
    // Flying words, then the card
    // ------------------------------------------------------------
    function flyWords() {
        words.forEach(function (word, i) {
            later(function () {
                const direction = DIRECTIONS[i % DIRECTIONS.length];
                word.style.setProperty('--fx', direction[0]);
                word.style.setProperty('--fy', direction[1]);
                word.style.setProperty('--rot', direction[2]);
                word.classList.remove('is-flying');
                void word.offsetWidth;  // restarts the animation when the popup is opened again
                word.classList.add('is-flying');
            }, 250 + i * WORD_GAP);
        });
        // The card rises as the last word starts to dissolve
        later(showCard, (words.length - 1) * WORD_GAP + WORD_FLIGHT);
    }

    function showCard() {
        popup.classList.add('is-final');
        const close = popup.querySelector('.cheer-close');
        if (close) close.focus({ preventScroll: true });
    }

    // ------------------------------------------------------------
    // Open / close
    // ------------------------------------------------------------
    function open() {
        popup.hidden = false;
        popup.classList.remove('is-final');
        document.documentElement.classList.add('promo-cheer-open');
        resize();
        popup.querySelector('.cheer-x').focus({ preventScroll: true });

        if (reduceMotion) {
            showCard();
            return;
        }
        running = true;
        lastTime = 0;
        window.requestAnimationFrame(frame);
        launch();
        later(launch, 180);
        later(launch, 380);
        later(keepLaunching, 700);
        flyWords();
    }

    function close() {
        running = false;
        timers.forEach(clearTimeout);
        timers = [];
        rockets = [];
        sparks = [];
        flashes = [];
        words.forEach(function (word) { word.classList.remove('is-flying'); });
        popup.hidden = true;
        popup.classList.remove('is-final');
        document.documentElement.classList.remove('promo-cheer-open');
        openButton.focus({ preventScroll: true });
    }

    openButton.addEventListener('click', open);
    closeButtons.forEach(function (button) {
        button.addEventListener('click', close);
    });

    // A tap anywhere outside the card and its buttons sets off a firework right there
    popup.addEventListener('click', function (event) {
        if (reduceMotion || !running) return;
        if (event.target.closest('.cheer-card, button, a')) return;
        explode(event.clientX, event.clientY);
    });

    // Escape closes; Tab stays inside the popup
    popup.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') {
            close();
            return;
        }
        if (event.key !== 'Tab') return;
        const focusable = Array.prototype.filter.call(popup.querySelectorAll('a[href], button'), function (el) {
            return el.offsetParent !== null && getComputedStyle(el).visibility !== 'hidden';
        });
        if (!focusable.length) return;
        const first = focusable[0];
        const last = focusable[focusable.length - 1];
        if (event.shiftKey && document.activeElement === first) {
            event.preventDefault();
            last.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
            event.preventDefault();
            first.focus();
        }
    });

    window.addEventListener('resize', function () {
        if (!popup.hidden) resize();
    });
});
