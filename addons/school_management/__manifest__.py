{
    "name": "School Management",
    "version": "16.0.1.0.0",
    "summary": "Full school management: students, teachers, classes, attendance, grades, fees.",
    "author": "Zayed",
    "category": "Education",
    "depends": ["base", "mail", "web_responsive", "base_user_role"],
    "icon": "/school_management/static/description/icon.svg",
    "data": [
        "security/groups.xml",
        "security/ir.model.access.csv",
        "views/menu.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}
