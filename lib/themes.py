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
    },
    "twilight": {
        "bg_primary": "#1e1e2e",
        "bg_secondary": "#313244",
        "text_primary": "#cdd6f4",
        "text_secondary": "#bac2de",
        "border": "#45475a",
        "success": "#a6e3a1",
        "info": "#89b4fa",
        "warning": "#f9e2af",
        "error": "#f38ba8",
        "accent_primary": "#cba6f7",
        "accent_secondary": "#b4befe",
        "scrollbar": "#45475a"
    },
    "blossom": {
        "bg_primary": "#fdf6e3",
        "bg_secondary": "#eee8d5",
        "text_primary": "#586e75",
        "text_secondary": "#657b83",
        "border": "#93a1a1",
        "success": "#859900",
        "info": "#268bd2",
        "warning": "#b58900",
        "error": "#dc322f",
        "accent_primary": "#d33682",
        "accent_secondary": "#6c71c4",
        "scrollbar": "#93a1a1"
    },
    "clarity": {
        "bg_primary": "#ffffff",
        "bg_secondary": "#f5f5f5",
        "text_primary": "#212121",
        "text_secondary": "#757575",
        "border": "#e0e0e0",
        "success": "#4caf50",
        "info": "#2196f3",
        "warning": "#ff9800",
        "error": "#f44336",
        "accent_primary": "#9c27b0",
        "accent_secondary": "#673ab7",
        "scrollbar": "#bdbdbd"
    },
    "pulse": {
        "bg_primary": "#0d1117",
        "bg_secondary": "#161b22",
        "text_primary": "#c9d1d9",
        "text_secondary": "#8b949e",
        "border": "#30363d",
        "success": "#238636",
        "info": "#58a6ff",
        "warning": "#d29922",
        "error": "#f85149",
        "accent_primary": "#1f6feb",
        "accent_secondary": "#388bfd",
        "scrollbar": "#30363d"
    },
    "vicuna": {
        "bg_primary": "#2b2520",
        "bg_secondary": "#3d3530",
        "text_primary": "#f5e6d3",
        "text_secondary": "#d4c5b0",
        "border": "#5a4a3f",
        "success": "#8fbc8f",
        "info": "#7db3d1",
        "warning": "#e89f4f",
        "error": "#d9534f",
        "accent_primary": "#d97536",
        "accent_secondary": "#c56426",
        "scrollbar": "#5a4a3f"
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
