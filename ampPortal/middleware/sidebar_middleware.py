from django.contrib import admin


class SidebarMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
    
    def get_import_export_models(self):
        registered_models = admin.site._registry
        has_import_export = {"import_export": []}
        
        for model, model_admin in registered_models.items():
                
            if hasattr(model_admin, "has_import_export"):
                has_import_export["import_export"].append(model._meta.verbose_name_plural.title().lower().replace(" ", ""))
        
        return has_import_export
        
    
    def get_apps_list(self):
        registered_models = admin.site._registry
        app_model_map = {}
        
        for model, model_admin in registered_models.items():
            app_label = model._meta.app_label
            
            if app_label not in app_model_map:
                app_model_map[app_label] = []
            
            app_model_map[app_label].append(model._meta.verbose_name_plural.title().lower().replace(" ", ""))
            

        return app_model_map

    def __call__(self, request):
    
        request.models_ctx = {"sidebar": self.get_apps_list(), "can_import": self.get_import_export_models() }
        
        response = self.get_response(request)
        return response