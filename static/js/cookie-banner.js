// Cookie consent banner (templates/core/cookie-banner.html).
//
// Klaviyo sets cookies that need the visitor's consent, so its script is only
// loaded after «Godta alle». The choice is kept in a first-party cookie for a
// year; the «Informasjonskapsler» button in the footer opens the banner again.

document.addEventListener('DOMContentLoaded', function () {
    const banner = document.getElementById('cookieBanner');
    if (!banner) return;

    const CONSENT_COOKIE = 'lfk_cookie_consent';
    const CONSENT_MAX_AGE = 60 * 60 * 24 * 365;  // one year, in seconds
    const CHOICE_LABELS = { all: 'Godta alle', necessary: 'Kun nødvendige' };
    // Cookie and storage names Klaviyo uses (__kla_id, __kla_viewed, klaviyoOnsite …)
    const KLAVIYO_PREFIXES = ['__kla', 'klaviyo'];

    const currentChoice = banner.querySelector('[data-cookie-current]');
    let klaviyoLoaded = false;
    let returnFocusTo = null;

    // ------------------------------------------------------------
    // The stored choice
    // ------------------------------------------------------------
    function readConsent() {
        const match = document.cookie.match(new RegExp('(?:^|; )' + CONSENT_COOKIE + '=([^;]*)'));
        const value = match ? match[1] : '';
        return CHOICE_LABELS.hasOwnProperty(value) ? value : '';
    }

    function saveConsent(choice) {
        let cookie = CONSENT_COOKIE + '=' + choice + '; Max-Age=' + CONSENT_MAX_AGE + '; Path=/; SameSite=Lax';
        if (location.protocol === 'https:') cookie += '; Secure';
        document.cookie = cookie;
    }

    // ------------------------------------------------------------
    // Klaviyo – the small queue stub in base.html is harmless; only
    // this script tag sets cookies
    // ------------------------------------------------------------
    function loadKlaviyo() {
        if (klaviyoLoaded) return;
        klaviyoLoaded = true;
        const script = document.createElement('script');
        script.async = true;
        script.src = banner.dataset.klaviyoSrc;
        document.head.appendChild(script);
    }

    function isKlaviyoName(name) {
        return KLAVIYO_PREFIXES.some(function (prefix) {
            return name.indexOf(prefix) === 0;
        });
    }

    // Klaviyo puts its cookies on the main domain (.lillehammerfk.no), so delete
    // them on every level of the host name as well as without a domain
    function removeKlaviyoData() {
        const parts = location.hostname.split('.');
        const domains = [''];
        for (let i = 0; i < parts.length - 1; i++) {
            domains.push('; Domain=' + parts.slice(i).join('.'));
        }

        document.cookie.split('; ').forEach(function (pair) {
            const name = pair.split('=')[0];
            if (!isKlaviyoName(name)) return;
            domains.forEach(function (domain) {
                document.cookie = name + '=; Max-Age=0; Path=/' + domain;
            });
        });

        [window.localStorage, window.sessionStorage].forEach(function (storage) {
            try {
                Object.keys(storage).forEach(function (key) {
                    if (isKlaviyoName(key)) storage.removeItem(key);
                });
            } catch (error) {
                // storage can be switched off in the browser; there is nothing to remove then
            }
        });
    }

    // ------------------------------------------------------------
    // Showing and hiding
    // ------------------------------------------------------------
    function openBanner(opener) {
        const consent = readConsent();
        currentChoice.hidden = !consent;
        currentChoice.textContent = consent ? 'Ditt valg nå: ' + CHOICE_LABELS[consent] + '.' : '';

        banner.hidden = false;
        document.documentElement.classList.add('cookie-banner-open');

        // Opened from the footer: move focus into the banner so keyboard users land on the choices
        returnFocusTo = opener || null;
        if (opener) banner.querySelector('[data-cookie-choice]').focus();
    }

    function closeBanner() {
        banner.hidden = true;
        document.documentElement.classList.remove('cookie-banner-open');
        if (returnFocusTo) returnFocusTo.focus();
        returnFocusTo = null;
    }

    banner.querySelectorAll('[data-cookie-choice]').forEach(function (button) {
        button.addEventListener('click', function () {
            const choice = button.dataset.cookieChoice;
            saveConsent(choice);

            if (choice === 'all') {
                loadKlaviyo();
                closeBanner();
                return;
            }

            removeKlaviyoData();
            closeBanner();
            // Klaviyo already runs on this page and would set its cookies again – a reload stops it
            if (klaviyoLoaded) location.reload();
        });
    });

    document.querySelectorAll('[data-cookie-settings]').forEach(function (button) {
        button.addEventListener('click', function () {
            openBanner(button);
        });
    });

    // Escape only closes the banner once a choice exists; the first time an answer is needed
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' && !banner.hidden && readConsent()) closeBanner();
    });

    // ------------------------------------------------------------
    // Start
    // ------------------------------------------------------------
    const consent = readConsent();
    if (consent === 'all') {
        loadKlaviyo();
    } else if (!consent) {
        openBanner();
    }
});
