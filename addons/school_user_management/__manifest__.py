{
    "name": "School User Management",
    "version": "16.0.1.0.0",
    "summary": "Manage school users and roles dynamically.",
    "author": "Zayed",
    "category": "Education",
    "depends": [
        "base",
        "base_user_role",  # res.users.role — dynamic role engine
        "school_management",  # school permission groups
    ],
    "icon": "/school_user_management/static/description/icon.svg",
    "data": [
        "security/ir.model.access.csv",
        "data/school_roles_data.xml",
        "views/school_role_views.xml",  # actions must load before menu
        "views/res_users_views.xml",
        "views/menu.xml",  # menu references actions — load last
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}
