"""Small XLSX exporters that preserve analytical engine outputs."""

from __future__ import annotations

from io import BytesIO
import re

import pandas as pd
from openpyxl.styles import Font


_INVALID_FILENAME_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


def _workbook_bytes(sheets: dict[str, pd.DataFrame]) -> bytes:
    """Return a simply formatted workbook without changing supplied values."""
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        for sheet_name, frame in sheets.items():
            frame.to_excel(writer, sheet_name=sheet_name, index=False)
            worksheet = writer.sheets[sheet_name]
            worksheet.freeze_panes = "A2"
            for cell in worksheet[1]:
                cell.font = Font(bold=True)
            for column_cells in worksheet.columns:
                width = max(len(str(cell.value or "")) for cell in column_cells) + 2
                worksheet.column_dimensions[column_cells[0].column_letter].width = min(width, 50)
    return buffer.getvalue()


def insurance_market_structure_workbook(
    summary: pd.DataFrame,
    source_table: pd.DataFrame,
) -> bytes:
    """Export the exact market-structure tables supplied by the engine."""
    summary_columns = ["year", "entity_count", "market_size", "cr1", "cr3", "cr5", "hhi", "known_data_break"]
    source_columns = [
        "year", "entity_id", "display_name", "market_value", "market_share", "rank", "included_flag", "exclusion_reason",
    ]
    methodology = pd.DataFrame(
        [
            ("Markedsgrundlag", "Res_BP_BeY / Bruttopræmier"),
            ("Enhed", "t.DKK"),
            ("Population", "Kun juridiske enheder med observerede positive bruttopræmier."),
            ("Koncentration", "CR1, CR3 og CR5 er kumulerede markedsandele; HHI er på skalaen 0-10.000."),
            ("Databrud", "2025 er et kendt dækningsbrud og bør fortolkes med forsigtighed."),
            ("Metode", "Se docs/MARKET_STRUCTURE_METHOD.md."),
        ],
        columns=["Emne", "Beskrivelse"],
    )
    return _workbook_bytes(
        {
            "Summary": summary.loc[:, summary_columns].copy(),
            "Market shares": source_table.loc[:, source_columns].copy(),
            "Methodology": methodology,
        }
    )


def bank_analyst_workbook(
    comparison: pd.DataFrame,
    history: pd.DataFrame,
    overview: dict,
    fiscal_year: int,
    benchmark_definition: str,
) -> bytes:
    """Export the exact comparison and history tables used by Bank Analyst View."""
    overview_table = pd.DataFrame(
        [
            ("Bank", overview["display_name"]),
            ("Enheds-ID", overview["entity_id"]),
            ("Regnr", overview["regnr"]),
            ("Valgt finansår", fiscal_year),
            ("Benchmark", benchmark_definition),
            ("Aktiver i alt (t.DKK)", overview["total_assets"]),
            ("Kernemetrikker med data", overview["metrics_with_data"]),
        ],
        columns=["Emne", "Værdi"],
    )
    comparison_columns = [
        "section", "metric_id", "display_name", "current_value", "previous_value", "yoy_change", "benchmark_median",
        "unit", "display_format", "source_type", "calculation_type", "validation_status", "definition",
    ]
    exported_comparison = comparison.rename(columns={"peer_median": "benchmark_median"})
    methodology = pd.DataFrame(
        [
            ("YoY", "Aktuel værdi minus samme metriks observerede værdi i umiddelbart foregående finansår."),
            ("Benchmark", f"{benchmark_definition}. Målbanken indgår, når den har data."),
            ("Identitet", "Kanonisk entity_id er baseret på regnr; displaynavn er kun en visningsattribut."),
            ("Manglende data", "Manglende observationer forbliver manglende og erstattes ikke med nul."),
            ("Proveniens", "Rapporterede og beregnede metrikker er angivet særskilt i sammenligningstabellen."),
            ("Udskudt", "Indlån, cost-income, indtjeningsvækst, kapitalprocenter og risikomål."),
            ("Metode", "Se docs/BANK_ANALYST_METHOD.md."),
        ],
        columns=["Emne", "Beskrivelse"],
    )
    return _workbook_bytes(
        {
            "Overview": overview_table,
            "Metric comparison": exported_comparison.loc[:, comparison_columns].copy(),
            "History": history.loc[:, ["metric_id", "fiscal_year", "value"]].copy(),
            "Methodology": methodology,
        }
    )


def insurance_market_structure_filename(start_year: int, end_year: int) -> str:
    return f"Databank_Insurance_Market_Structure_{start_year}-{end_year}.xlsx"


def bank_analyst_filename(display_name: str, fiscal_year: int) -> str:
    """Return a deterministic Windows-safe bank export filename."""
    safe_name = _INVALID_FILENAME_CHARS.sub("_", str(display_name))
    safe_name = re.sub(r"\s+", "_", safe_name).strip("._ ") or "Bank"
    return f"Databank_Bank_Analyst_{safe_name}_{fiscal_year}.xlsx"
