# Application module registry

Register a new application-facing workspace in `modules/registry.py` with a stable
`module_id`, display metadata, ordering, and a small render adapter. Map its
navigation view type in `VIEW_TYPE_MODULE_IDS`; the renderer belongs in `views/`,
not in analytics modules. `app.py` then dispatches it without a new branch.
