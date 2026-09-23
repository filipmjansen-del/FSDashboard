"""Pure value and Plotly formatting helpers."""

import pandas as pd

from ui.theme import BEIGE, BLACK, GREY_DARK, GREY_LIGHT, PURPLE, WHITE


def format_kpi_value(value, meta):
    if pd.isna(value):
        return "–"
    display_format = meta.get("display_format", "number")
    decimals = meta.get("decimals", 2)
    if display_format == "multiple":
        return f"{value:.{decimals}f}x"
    if display_format == "percentage":
        return f"{value:.{decimals}%}"
    if display_format == "integer":
        return f"{value:,.0f}"
    if display_format == "dkk":
        return f"DKK {value:,.{decimals}f}"
    if display_format == "dkk_million":
        return f"DKK {value / 1_000_000:,.{decimals}f} mio."
    if display_format == "dkk_billion":
        return f"DKK {value / 1_000_000_000:,.{decimals}f} mia."
    return f"{value:,.{decimals}f}"


def apply_kpi_axis_format(fig, meta, axis="y"):
    display_format = meta.get("display_format", "number")
    decimals = meta.get("decimals", 2)
    if display_format == "multiple":
        settings = {"tickformat": f".{decimals}f", "ticksuffix": "x"}
    elif display_format == "percentage":
        settings = {"tickformat": f".{decimals}%"}
    elif display_format == "integer":
        settings = {"tickformat": ",.0f"}
    elif display_format == "dkk":
        settings = {"tickformat": f",.{decimals}f", "tickprefix": "DKK "}
    elif display_format in {"dkk_million", "dkk_billion"}:
        settings = {"tickformat": ".3s", "tickprefix": "DKK "}
    else:
        settings = {"tickformat": f",.{decimals}f"}
    (fig.update_xaxes if axis == "x" else fig.update_yaxes)(**settings)
    return fig


def get_plotly_hover_format(meta):
    display_format = meta.get("display_format", "number")
    decimals = meta.get("decimals", 2)
    if display_format == "percentage":
        return f":.{decimals}%"
    if display_format == "multiple":
        return f":.{decimals}f"
    if display_format == "integer":
        return ":,.0f"
    return f":,.{decimals}f"


def brand_plotly(fig, *, legend_title=None):
    fig.update_layout(
        template="plotly_white", paper_bgcolor=WHITE, plot_bgcolor=WHITE,
        font=dict(color=BLACK, family="Arial"), title_font=dict(color=PURPLE),
        legend_title_text=legend_title,
        legend=dict(bgcolor="rgba(255,255,255,0)", font=dict(color=BLACK)),
        margin=dict(l=20, r=20, t=40, b=20),
        hoverlabel=dict(bgcolor=PURPLE, font_color=WHITE, bordercolor=PURPLE),
    )
    fig.update_xaxes(showgrid=False, linecolor=BEIGE, tickfont=dict(color=BLACK),
                     title_font=dict(color=GREY_DARK), zeroline=False)
    fig.update_yaxes(gridcolor=GREY_LIGHT, linecolor=BEIGE, tickfont=dict(color=BLACK),
                     title_font=dict(color=GREY_DARK), zeroline=False)
    return fig
