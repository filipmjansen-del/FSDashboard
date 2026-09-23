import unittest

from modules.registry import MODULE_REGISTRY, module_id_for


class ModuleRegistryTests(unittest.TestCase):
    def test_existing_workspaces_have_stable_registered_ids(self):
        self.assertEqual(
            set(MODULE_REGISTRY),
            {"home", "kpi_workspace", "dashboard_workspace"},
        )

    def test_navigation_view_types_resolve_to_registered_modules(self):
        self.assertEqual(module_id_for(None, None), "home")
        self.assertEqual(module_id_for("kpi", "Income / Cost"), "kpi_workspace")
        self.assertEqual(module_id_for("dashboard", "Income mix"), "dashboard_workspace")


if __name__ == "__main__":
    unittest.main()
