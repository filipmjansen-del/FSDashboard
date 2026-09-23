"""Small registry for application-level Streamlit modules."""

from dataclasses import dataclass
from typing import Callable

from views.dashboard_workspace import render_dashboard_workspace
from views.home import render_home
from views.kpi_workspace import render_kpi_workspace


@dataclass(frozen=True)
class ModuleContext:
    selected_industry: str | None
    selected_view_name: str | None
    get_raw_data: Callable
    get_kpi_data: Callable
    navigate_to: Callable
    industries: Callable


@dataclass(frozen=True)
class ApplicationModule:
    module_id: str
    label: str
    section: str
    order: int
    render: Callable[[ModuleContext], None]


def _render_home(context: ModuleContext):
    render_home(
        context.get_raw_data(),
        context.get_kpi_data,
        context.navigate_to,
        context.industries(),
    )


def _render_kpi_workspace(context: ModuleContext):
    render_kpi_workspace(
        context.selected_industry,
        context.selected_view_name,
        context.get_kpi_data,
    )


def _render_dashboard_workspace(context: ModuleContext):
    render_dashboard_workspace(
        context.selected_industry,
        context.selected_view_name,
        context.get_raw_data,
    )


MODULE_REGISTRY = {
    "home": ApplicationModule("home", "Navigationsoversigt", "navigation", 10, _render_home),
    "kpi_workspace": ApplicationModule("kpi_workspace", "KPI", "workspace", 20, _render_kpi_workspace),
    "dashboard_workspace": ApplicationModule(
        "dashboard_workspace", "Analyse", "workspace", 30, _render_dashboard_workspace
    ),
}

VIEW_TYPE_MODULE_IDS = {"kpi": "kpi_workspace", "dashboard": "dashboard_workspace"}


def module_id_for(view_type: str | None, view_name: str | None) -> str | None:
    return "home" if view_name is None else VIEW_TYPE_MODULE_IDS.get(view_type)


def dispatch_module(module_id: str | None, context: ModuleContext):
    if module_id is not None:
        MODULE_REGISTRY[module_id].render(context)
