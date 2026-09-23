# Application module registry

To add an application-facing analytical workspace:

1. Create its renderer in `views/`; keep analytics and calculations outside it.
2. Add a small adapter and `ApplicationModule` entry in `modules/registry.py` with a stable `module_id`, label, section, and order.
3. Map its navigation view type in `VIEW_TYPE_MODULE_IDS`.

`app.py` dispatches the registered module without a new module-specific branch.
