from enum import Enum
class Sidebar:
    sidebar_items = {
            "Dashboard Overview": {
                "icon": "fas fa-desktop",
                "sub_items": {
                    "Company dashboard": {"icon": "fa fa-truck", "url": "/dashboard/home/"},
                    "Transport Dashboard": {"icon": "fa fa-truck", "url": "/dashboard/transport/"},
                    "Inventory Dashboard": {"icon": "fa fa-boxes", "url": "/dashboard/inventory/"},
                    "Warehouse Dashboard": {"icon": "fa fa-warehouse", "url": "/dashboard/warehouse/"},
                    "Tracking Dashboard": {"icon": "fa fa-map-marked-alt", "url": "/dashboard/tracking/"},
                },
            },
            
            "Employees Management": {
            "icon": "fa fa-users",
            "sub_items": {
                "View Employees": {"icon": "fa fa-list", "url": "/employees/employee-list/"},
                "Requested Inventories": {"icon": "fa fa-plus", "url": "/inventory/requested-inventory/"},
                "Manage Departments": {"icon": "fa fa-building", "url": "/employees/departments/"},
                # "Assign Roles": {"icon": "fa fa-user-shield", "url": "/employees/roles/"},
            },
        },

            "Inventory Management": {
                "icon": "fa fa-box-open",
                "sub_items": {
                    "View All Inventory": {"icon": "fa fa-list", "url": "/inventory/view-inventories/"},
                    "Inventory Requests": {"icon": "fa fa-plus", "url": "/inventory/requested-inventory/"},
                    "Inventory Transactions": {"icon": "fa fa-exclamation-circle", "url":"/inventory/alerts/"},
                },
            },

            "Warehouse Operations": {
                "icon": "fa fa-warehouse",
                "sub_items": {
                    "Warehouse Overview": {"icon": "fa fa-info-circle", "url": "/warehouse/overview/"},
                    "Storage Management": {"icon": "fa fa-box", "url": "/warehouse/storage/"},
                    "Inbound Shipments": {"icon": "fa fa-arrow-down", "url": "/warehouse/inbound/"},
                    "Outbound Shipments": {"icon": "fa fa-arrow-up", "url": "/warehouse/outbound/"},
                },
            },

            "Transport & Logistics": {
            "icon": "fa fa-truck",
            "sub_items": {
                "Fleet Overview": {"icon": "fa fa-car-side", "url": "/transport/vehicles/"},
                "Dispatch Overview": {"icon": "fa fa-calendar", "url": "/transport/delivery_schedule/"},
                "Fleet Management": {"icon": "fa fa-user-tag", "url": "/transport/driver_assistant_assignment/"},
                "Client Request Records": {"icon": "fa fa-handshake", "url": "/transport/client-requests/"},
                "Maintenance Records": {"icon": "fa fa-tools", "url": "/transport/maintenance-request/"},
                "Requested Inventories": {"icon": "fa fa-plus", "url": "/transport/inventory/view/"},
            }
        }
        ,

            "Real-Time Tracking": {
                "icon": "fa fa-map",
                "sub_items": {
                    "Track Vehicles": {"icon": "fa fa-truck-moving", "url": "/tracking/vehicles/"},
                    "Track Shipments": {"icon": "fa fa-shipping-fast", "url": "/tracking/shipments/"},
                    "Route Optimization": {"icon": "fa fa-route", "url": "/tracking/routes/"},
                    "Historical Route Data": {"icon": "fa fa-history", "url": "/tracking/history/"},
                },
            },

            "Insights & Reports": {
                "icon": "fa fa-chart-line",
                "sub_items": {
                    "Sales Reports": {"icon": "fa fa-file-invoice-dollar", "url": "/reports/sales/"},
                    "Stock Reports": {"icon": "fa fa-clipboard-list", "url": "/reports/stock/"},
                    "Transport Efficiency": {"icon": "fa fa-road", "url": "/reports/transport/"},
                    "Warehouse Utilization": {"icon": "fa fa-boxes", "url": "/reports/warehouse/"},
                },
            },

            "Security & Access Control": {
                "icon": "fa fa-shield-alt",
                "sub_items": {
                    "User Roles & Permissions": {"icon": "fa fa-user-shield", "url": "/security/roles/"},
                    "Login History & Logs": {"icon": "fa fa-history", "url": "/security/logs/"},
                    "Two-Factor Authentication": {"icon": "fa fa-lock", "url": "/security/2fa/"},
                },
            },

            "Settings & Configuration": {
                "icon": "fa fa-cogs",
                "sub_items": {
                    "User Accounts": {"icon": "fa fa-user-cog", "url": "/settings/users/"},
                    "System Preferences": {"icon": "fa fa-sliders-h", "url": "/settings/system/"},
                    "Notifications & Alerts": {"icon": "fa fa-bell", "url": "/settings/notifications/"},
                },
            },

            "Logout": {
                "icon": "fa fa-sign-out-alt",
                "url": "/logout/",
            },
        }



        