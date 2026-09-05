THEMES = {
    "Cyber Indigo (Dark)": {
        "bg_base": "#090D16",
        "bg_gradient_1": "rgba(99, 102, 241, 0.20)",
        "bg_gradient_2": "rgba(168, 85, 247, 0.14)",
        "bg_gradient_3": "rgba(56, 189, 248, 0.10)",
        "card_bg": "rgba(15, 23, 42, 0.70)",
        "card_border": "rgba(255, 255, 255, 0.08)",
        "card_hover_border": "rgba(99, 102, 241, 0.5)",
        "text_main": "#F8FAFC",
        "text_sub": "#94A3B8",
        "accent_primary": "#6366F1",
        "accent_secondary": "#A855F7",
        "accent_cyan": "#38BDF8",
        "cursor_color": "%23818CF8",
        "input_bg": "rgba(15, 23, 42, 0.85)"
    },
    "Emerald Matrix (Dark)": {
        "bg_base": "#06120D",
        "bg_gradient_1": "rgba(16, 185, 129, 0.22)",
        "bg_gradient_2": "rgba(5, 150, 105, 0.15)",
        "bg_gradient_3": "rgba(52, 211, 153, 0.10)",
        "card_bg": "rgba(9, 28, 20, 0.75)",
        "card_border": "rgba(52, 211, 153, 0.15)",
        "card_hover_border": "rgba(16, 185, 129, 0.6)",
        "text_main": "#ECFDF5",
        "text_sub": "#6EE7B7",
        "accent_primary": "#10B981",
        "accent_secondary": "#059669",
        "accent_cyan": "#34D399",
        "cursor_color": "%2334D399",
        "input_bg": "rgba(8, 24, 18, 0.85)"
    },
    "Solar Flare (Dark)": {
        "bg_base": "#120B04",
        "bg_gradient_1": "rgba(245, 158, 11, 0.22)",
        "bg_gradient_2": "rgba(234, 88, 12, 0.16)",
        "bg_gradient_3": "rgba(251, 191, 36, 0.10)",
        "card_bg": "rgba(28, 17, 8, 0.75)",
        "card_border": "rgba(251, 191, 36, 0.15)",
        "card_hover_border": "rgba(245, 158, 11, 0.6)",
        "text_main": "#FFFBEB",
        "text_sub": "#FCD34D",
        "accent_primary": "#F59E0B",
        "accent_secondary": "#EA580C",
        "accent_cyan": "#FBBF24",
        "cursor_color": "%23FBBF24",
        "input_bg": "rgba(24, 14, 6, 0.85)"
    },
    "Frost Quantum (Light)": {
        "bg_base": "#F1F5F9",
        "bg_gradient_1": "rgba(99, 102, 241, 0.12)",
        "bg_gradient_2": "rgba(56, 189, 248, 0.14)",
        "bg_gradient_3": "rgba(168, 85, 247, 0.08)",
        "card_bg": "rgba(255, 255, 255, 0.85)",
        "card_border": "rgba(99, 102, 241, 0.18)",
        "card_hover_border": "rgba(99, 102, 241, 0.6)",
        "text_main": "#0F172A",
        "text_sub": "#475569",
        "accent_primary": "#4F46E5",
        "accent_secondary": "#7C3AED",
        "accent_cyan": "#0284C7",
        "cursor_color": "%234F46E5",
        "input_bg": "#FFFFFF"
    }
}

def get_theme_css(theme_name: str) -> str:
    t = THEMES.get(theme_name, THEMES["Cyber Indigo (Dark)"])
    c = t['cursor_color']

    # Custom SVG Reticle pointers encoded directly into CSS (zero script dependency)
    # Default Cross-Dot Cursor:
    default_cursor = f"url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24'%3E%3Ccircle cx='12' cy='12' r='4' fill='{c}'/%3E%3Ccircle cx='12' cy='12' r='8' stroke='{c}' stroke-width='1.5' fill='none' opacity='0.7'/%3E%3C/svg%3E\") 12 12, auto"
    
    # Pointer / Hover Target Cursor (Target Lock):
    pointer_cursor = f"url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='28' height='28' viewBox='0 0 28 28'%3E%3Ccircle cx='14' cy='14' r='3' fill='{c}'/%3E%3Ccircle cx='14' cy='14' r='10' stroke='{c}' stroke-width='2' stroke-dasharray='4,3' fill='none'/%3E%3C/svg%3E\") 14 14, pointer"

    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Fira+Code:wght@400;600&display=swap');

:root {{
    --bg-base: {t['bg_base']};
    --card-bg: {t['card_bg']};
    --card-border: {t['card_border']};
    --card-hover-border: {t['card_hover_border']};
    --text-main: {t['text_main']};
    --text-sub: {t['text_sub']};
    --accent-primary: {t['accent_primary']};
    --accent-secondary: {t['accent_secondary']};
    --accent-cyan: {t['accent_cyan']};
    --input-bg: {t['input_bg']};
}}

/* Guaranteed Visible Custom Cyber Reticle */
html, body, .stApp {{
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    cursor: {default_cursor} !important;
    background: 
        radial-gradient(ellipse 80% 50% at 50% -20%, {t['bg_gradient_1']} 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 85% 90%, {t['bg_gradient_2']} 0%, transparent 60%),
        radial-gradient(ellipse 50% 30% at 10% 80%, {t['bg_gradient_3']} 0%, transparent 50%),
        var(--bg-base);
    color: var(--text-main);
    overflow-x: hidden;
    transition: background 0.4s ease, color 0.4s ease;
}}

/* Clickable Targets & Buttons: Target Reticle Pointer */
button, .stButton>button, [role="button"], [data-baseweb="tab"], .pill-tag {{
    cursor: {pointer_cursor} !important;
}}

/* Text Fields: Guaranteed I-Beam Cursor */
input, textarea, .stTextInput input, .stTextArea textarea {{
    cursor: text !important;
}}

/* Gauges & Telemetry: Zoom / Inspection Cursor */
.gauge-box, .hero-wrapper {{
    cursor: crosshair !important;
}}

/* Interactive Glass Cards */
.panel-card, .hero-wrapper {{
    background: var(--card-bg) !important;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border: 1px solid var(--card-border) !important;
    border-radius: 22px;
    padding: 1.8rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.25);
    transition: border-color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
}}

.panel-card:hover {{
    border-color: var(--card-hover-border) !important;
    box-shadow: 0 20px 45px rgba(0, 0, 0, 0.35);
}}

/* Button Styling & Hover Physics */
.stButton>button {{
    background: var(--card-bg) !important;
    color: var(--text-main) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 14px !important;
    font-weight: 600 !important;
    padding: 0.65rem 1.2rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
}}

.stButton>button:hover {{
    transform: translateY(-3px) scale(1.01) !important;
    border-color: var(--accent-primary) !important;
    box-shadow: 0 10px 25px rgba(99, 102, 241, 0.35) !important;
}}

.stButton>button:active {{
    transform: translateY(0px) scale(0.98) !important;
}}

/* Primary Action Buttons */
.stButton>button[kind="primary"] {{
    background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    box-shadow: 0 8px 25px rgba(99, 102, 241, 0.45) !important;
}}

.stButton>button[kind="primary"]:hover {{
    box-shadow: 0 12px 30px rgba(99, 102, 241, 0.65) !important;
    transform: translateY(-3px) scale(1.02) !important;
}}

/* Input Controls */
.stTextInput>div>div>input, .stTextArea>div>div>textarea {{
    background-color: var(--input-bg) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 14px !important;
    color: var(--text-main) !important;
    transition: all 0.25s ease !important;
}}

.stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {{
    border-color: var(--accent-primary) !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25) !important;
}}

/* Telemetry Gauges */
.gauge-box {{
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid var(--card-border);
    border-radius: 18px;
    padding: 1.2rem;
    text-align: center;
    transition: all 0.25s ease;
}}

.gauge-box:hover {{
    border-color: var(--accent-cyan);
    transform: scale(1.02);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}}

.gauge-score {{
    font-size: 2.2rem;
    font-weight: 800;
    font-family: 'Fira Code', monospace;
    background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.gauge-label {{
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--text-sub);
    text-transform: uppercase;
    letter-spacing: 0.06em;
}}

.hero-tag {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 9999px;
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid var(--card-border);
    color: var(--accent-cyan);
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}}

.hero-title {{
    font-size: 2.8rem;
    font-weight: 800;
    line-height: 1.15;
    letter-spacing: -0.03em;
    margin: 0 0 0.8rem 0;
    background: linear-gradient(135deg, var(--text-main) 30%, var(--accent-cyan) 80%, var(--accent-primary) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.hero-subtitle {{
    font-size: 1.1rem;
    color: var(--text-sub);
    max-width: 680px;
    line-height: 1.6;
}}

.pill-tag {{
    display: inline-block;
    padding: 5px 12px;
    border-radius: 8px;
    font-size: 0.78rem;
    font-weight: 600;
    margin: 0 6px 6px 0;
}}

.pill-gap {{
    background: rgba(239, 68, 68, 0.15);
    color: #F87171;
    border: 1px solid rgba(239, 68, 68, 0.3);
}}

.pill-jargon {{
    background: rgba(245, 158, 11, 0.15);
    color: #FBBF24;
    border: 1px solid rgba(245, 158, 11, 0.3);
}}
</style>
"""

def get_trailing_follower_js() -> str:
    """Provides an optional smooth trailing glow circle without breaking the primary visible cursor."""
    return """
    <div id="trail-halo" style="
        position: fixed;
        width: 32px;
        height: 32px;
        border: 1.5px solid rgba(99, 102, 241, 0.5);
        border-radius: 50%;
        pointer-events: none;
        transform: translate(-50%, -50%);
        z-index: 999999;
        transition: width 0.2s ease, height 0.2s ease;
    "></div>
    <script>
    (function() {
        const halo = document.getElementById('trail-halo');
        let mouseX = 0, mouseY = 0, posX = 0, posY = 0;
        
        window.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
        });
        
        function loop() {
            posX += (mouseX - posX) * 0.2;
            posY += (mouseY - posY) * 0.2;
            halo.style.left = posX + 'px';
            halo.style.top = posY + 'px';
            requestAnimationFrame(loop);
        }
        loop();
    })();
    </script>
    """