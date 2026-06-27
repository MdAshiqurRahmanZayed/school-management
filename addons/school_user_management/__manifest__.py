{
    "name": "School User Management",
    "version": "16.0.1.0.0",
    "summary": "User management for school administrators and principals.",
    "author": "Zayed",
    "category": "Education",
    "depends": ["base", "base_user_role", "school_management"],
    "data": [
        "security/ir.model.access.csv",
        "data/school_roles_data.xml",
        "views/menu.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}
