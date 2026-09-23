import unittest

from modules.registry import MODULE_REGISTRY, module_id_for
from views.dashboard_workspace import render_dashboard_workspace
from views.home import render_home
from views.kpi_workspace import render_kpi_workspace


class ApplicationModuleSmokeTests(unittest.TestCase):
    def test_registered_workspaces_resolve_to_existing_view_renderers(self):
        expected = {
            "home": render_home,
            "kpi_workspace": render_kpi_workspace,
            "dashboard_workspace": render_dashboard_workspace,
        }
        self.assertEqual(set(MODULE_REGISTRY), set(expected))
        for module_id, renderer in expected.items():
            self.assertTrue(callable(MODULE_REGISTRY[module_id].render))
            self.assertTrue(callable(renderer))

    def test_registered_navigation_types_are_accessible(self):
        self.assertEqual(module_id_for(None, None), "home")
        self.assertIn(module_id_for("kpi", "example"), MODULE_REGISTRY)
        self.assertIn(module_id_for("dashboard", "example"), MODULE_REGISTRY)


if __name__ == "__main__":
    unittest.main()
