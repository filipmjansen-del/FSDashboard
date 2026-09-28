"""Pure value and Plotly formatting helpers."""

import pandas as pd

from ui.theme import BEIGE, BLACK, GREY_DARK, GREY_LIGHT, PURPLE, WHITE


PLOTLY_PNG_WIDTH = 1600
PLOTLY_PNG_HEIGHT = 900


def format_danish_number(value, decimals: int = 0, *, signed: bool = False) -> str:
    """Format a number for Danish-facing UI without changing its value."""
    sign = "+" if signed else ""
    rendered = f"{value:{sign},.{decimals}f}"
    return rendered.replace(",", "X").replace(".", ",").replace("X", ".")


def format_kpi_value(value, meta):
    if pd.isna(value):
        return "–"
    display_format = meta.get("display_format", "number")
    decimals = meta.get("decimals", 2)
    if display_format == "multiple":
        return f"{format_danish_number(value, decimals)}x"
    if display_format == "percentage":
        return f"{format_danish_number(value * 100, decimals)} %"
    if display_format == "integer":
        return format_danish_number(value)
    if display_format == "dkk":
        return f"DKK {format_danish_number(value, decimals)}"
    if display_format == "dkk_million":
        return f"DKK {format_danish_number(value / 1_000_000, decimals)} mio."
    if display_format == "dkk_billion":
        return f"DKK {format_danish_number(value / 1_000_000_000, decimals)} mia."
    if display_format == "dkk_billion_tdk":
        return f"DKK {format_danish_number(value / 1_000_000, decimals)} mia."
    return format_danish_number(value, decimals)


def format_kpi_delta(value, meta):
    """Format a year-on-year absolute change without treating missing as zero."""
    if pd.isna(value):
        return "–"
    display_format = meta.get("display_format", "number")
    decimals = meta.get("decimals", 2)
    if display_format == "percentage":
        return f"{format_danish_number(value * 100, decimals, signed=True)} pp"
    if display_format == "multiple":
        return f"{format_danish_number(value, decimals, signed=True)}x"
    if display_format == "dkk_billion_tdk":
        return f"DKK {format_danish_number(value / 1_000_000, decimals, signed=True)} mia."
    return format_danish_number(value, decimals, signed=True)


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


def plotly_export_config(filename: str) -> dict:
    """Return a PowerPoint-ready PNG export configuration for Plotly modebars."""
    return {
        "displaylogo": False,
        "toImageButtonOptions": {
            "format": "png",
            "filename": filename,
            "width": PLOTLY_PNG_WIDTH,
            "height": PLOTLY_PNG_HEIGHT,
            "scale": 1,
        },
    }


def brand_plotly(fig, *, legend_title=None, subtitle: str | None = None):
    title_text = fig.layout.title.text or ""
    if subtitle:
        title_text = f"{title_text}<br><sup>{subtitle}</sup>" if title_text else subtitle
    fig.update_layout(
        template="plotly_white", paper_bgcolor=WHITE, plot_bgcolor=WHITE,
        font=dict(color=BLACK, family="Arial", size=13), title_font=dict(color=PURPLE, size=18),
        title=dict(text=title_text, x=0, xanchor="left"),
        legend_title_text=legend_title,
        legend=dict(bgcolor="rgba(255,255,255,0)", font=dict(color=BLACK)),
        margin=dict(l=12, r=20, t=58, b=28),
        hoverlabel=dict(bgcolor=PURPLE, font_color=WHITE, bordercolor=PURPLE),
    )
    fig.update_xaxes(showgrid=False, linecolor=BEIGE, tickfont=dict(color=BLACK),
                     title_font=dict(color=GREY_DARK), zeroline=False, fixedrange=True)
    fig.update_yaxes(gridcolor=GREY_LIGHT, linecolor=BEIGE, tickfont=dict(color=BLACK),
                     title_font=dict(color=GREY_DARK), zeroline=False, fixedrange=True)
    fig.update_traces(selector={"type": "scatter"}, line={"width": 2.4}, marker={"size": 6})
    return fig
