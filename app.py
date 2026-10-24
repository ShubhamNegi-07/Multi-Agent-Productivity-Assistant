
processing = st.session_state.pending is not None

# ─── Design System ────────────────────────────────────────────────────────────
BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    /* Canvas + surfaces — Tailwind slate, cool and low-chroma. */
    --bg:          #F8FAFC;
    --surface:     #FFFFFF;
    --surface-2:   #F1F5F9;
    --surface-3:   #E2E8F0;

    /* Hairlines */
    --line:        #E2E8F0;
    --line-soft:   #F1F5F9;

    /* Ink ramp */
    --ink:         #0F172A;
    --ink-2:       #475569;
    --ink-3:       #94A3B8;

    /* The single primary. Everything interactive lands here. */
    --primary:      #4F46E5;
    --primary-hi:   #4338CA;
    --primary-tint: #EEF2FF;
    --primary-edge: #E0E7FF;
    --on-primary:   #FFFFFF;

    /* Status */
    --danger:      #DC2626;
    --danger-tint: #FEF2F2;
    --danger-edge: #FECACA;
    --live:        #16A34A;

    /* Elevation — soft and short, never muddy. */
    --shadow-xs: 0 1px 2px rgba(15, 23, 42, 0.05);
    --shadow-sm: 0 1px 3px rgba(15, 23, 42, 0.06), 0 1px 2px rgba(15, 23, 42, 0.04);
    --shadow-md: 0 4px 14px rgba(15, 23, 42, 0.07), 0 1px 3px rgba(15, 23, 42, 0.04);
    --shadow-lg: 0 14px 40px rgba(15, 23, 42, 0.12), 0 2px 8px rgba(15, 23, 42, 0.05);
    --ring:      0 0 0 3px rgba(79, 70, 229, 0.18);

    --r-sm: 8px;
    --r-md: 12px;
    --r-lg: 16px;
    --r-xl: 20px;

    --sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
            Helvetica, Arial, sans-serif;
}

html, body, [class*="css"], button, input, textarea, select {
    font-family: var(--sans);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

[data-testid="stAppViewContainer"],
[data-testid="stMain"] {