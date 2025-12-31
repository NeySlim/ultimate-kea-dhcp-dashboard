"""Theme definitions for Ultimate Dashboard"""

THEMES = {
    "ember": {
        "bg_primary": "#1a1515",
        "bg_secondary": "#2d2424",
        "text_primary": "#e8d5b7",
        "text_secondary": "#b89968",
        "border": "#4a3f35",
        "success": "#87a987",
        "info": "#88c0d0",
        "warning": "#d4a574",
        "error": "#c17b6f",
        "accent_primary": "#b4a582",
        "accent_secondary": "#9d8b6a",
        "scrollbar": "#4a3f35"
    },
    "aurora": {
        "bg_primary": "#2e3440",
        "bg_secondary": "#3b4252",
        "text_primary": "#eceff4",
        "text_secondary": "#d8dee9",
        "border": "#4c566a",
        "success": "#a3be8c",
        "info": "#88c0d0",
        "warning": "#ebcb8b",
        "error": "#bf616a",
        "accent_primary": "#81a1c1",
        "accent_secondary": "#5e81ac",
        "scrollbar": "#4c566a"
    },
    "frost": {
        "bg_primary": "#e5e9f0",
        "bg_secondary": "#d8dee9",
        "text_primary": "#2e3440",
        "text_secondary": "#4c566a",
        "border": "#d8dee9",
        "success": "#a3be8c",
        "info": "#5e81ac",
        "warning": "#ebcb8b",
        "error": "#bf616a",
        "accent_primary": "#88c0d0",
        "accent_secondary": "#81a1c1",
        "scrollbar": "#4c566a"
    }
}


def get_theme_css(theme_name="ember"):
    """Generate CSS for a specific theme"""
    t = THEMES.get(theme_name, THEMES["ember"])
    
    return f"""
        body {{
            background: {t['bg_primary']};
            color: {t['text_primary']};
        }}
        h1 {{
            color: {t['text_primary']};
        }}
        .container {{
            background: {t['bg_secondary']};
            border-color: {t['border']};
        }}
        .pool-box {{
            background: {t['bg_secondary']};
            border-color: {t['border']};
        }}
        .pool-name {{
            color: {t['accent_primary']};
        }}
        table {{
            border-color: {t['border']};
        }}
        th {{
            background: rgba({int(t['bg_primary'][1:3], 16)}, {int(t['bg_primary'][3:5], 16)}, {int(t['bg_primary'][5:7], 16)}, 0.8);
            color: {t['text_primary']};
            border-color: {t['border']};
        }}
        td {{
            border-color: {t['border']};
            color: {t['text_primary']};
        }}
        tr:hover {{
            background: rgba({int(t['accent_primary'][1:3], 16)}, {int(t['accent_primary'][3:5], 16)}, {int(t['accent_primary'][5:7], 16)}, 0.1);
        }}
        .active {{
            background: rgba({int(t['success'][1:3], 16)}, {int(t['success'][3:5], 16)}, {int(t['success'][5:7], 16)}, 0.2);
        }}
        .expired {{
            background: rgba({int(t['error'][1:3], 16)}, {int(t['error'][3:5], 16)}, {int(t['error'][5:7], 16)}, 0.2);
        }}
        .timestamp {{
            color: {t['text_secondary']};
        }}
        .info {{
            background: {t['bg_secondary']};
            border-color: {t['border']};
        }}
        .info a {{
            color: {t['info']};
        }}
        .info a:hover {{
            color: {t['accent_secondary']};
        }}
        .gauge-container {{
            border-color: {t['border']};
            background: rgba({int(t['bg_secondary'][1:3], 16)}, {int(t['bg_secondary'][3:5], 16)}, {int(t['bg_secondary'][5:7], 16)}, 0.5);
        }}
        .stat-label {{
            color: {t['text_secondary']};
        }}
        .gauge-bg {{
            stroke: {t['border']};
        }}
        .gauge-value {{
            fill: {t['text_primary']};
        }}
        .gauge-legend {{
            color: {t['text_primary']};
        }}
        .cpu-core-0-fill {{
            stroke: {t['success']};
        }}
        .cpu-core-1-fill {{
            stroke: {t['info']};
        }}
        .cpu-core-2-fill {{
            stroke: {t['warning']};
        }}
        .cpu-core-3-fill {{
            stroke: {t['accent_primary']};
        }}
        #ramGaugeFill {{
            stroke: {t['info']};
        }}
        #netGaugeFillSend {{
            stroke: {t['success']};
        }}
        #netGaugeFillRecv {{
            stroke: {t['accent_primary']};
        }}
        #diskGaugeFill {{
            stroke: {t['error']};
        }}
        ::-webkit-scrollbar-thumb {{
            background: {t['scrollbar']};
        }}
        ::-webkit-scrollbar-track {{
            background: {t['bg_primary']};
        }}
    """
