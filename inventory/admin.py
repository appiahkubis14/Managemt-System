from django.contrib import admin
from .models import (
    InventoryItem, Fuel, Lubricant, Machinery, OfficeEquipment, 
    Stationery, InventoryRequest,InventoryItem
)


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity', 'reorder_level')
    list_filter = ('category',)
    search_fields = ('name', 'category',)
    ordering = ('name',)
    
    def reorder_level(self, obj):
        
        return "Low" if obj.quantity < 10 else "Sufficient"
    reorder_level.short_description = "Reorder Level"

from django.contrib import admin
from .models import InventoryRequest

@admin.register(InventoryRequest)
class InventoryRequestAdmin(admin.ModelAdmin):
    ordering = ["created_at"]
    list_display = [
        "item", "category", "quantity", "transaction_type",
        "from_department", "to_department", "employee_name",
        "employee_gender", "employee_phone", "employee_ghana_card_number",
        "employee_position", "created_at", "remarks"
    ]
    list_filter = ["transaction_type", "created_at"]




@admin.register(Fuel)
class FuelAdmin(admin.ModelAdmin):
    list_display = ("inventory_item", "fuel_type", "storage_capacity")

@admin.register(Lubricant)
class LubricantAdmin(admin.ModelAdmin):
    list_display = ("inventory_item", "viscosity_grade", "application_area")

@admin.register(Machinery)
class MachineryAdmin(admin.ModelAdmin):
    list_display = ("inventory_item", "machine_type", "manufacturer", "model_number")
    search_fields = ("machine_type", "model_number")

@admin.register(OfficeEquipment)
class OfficeEquipmentAdmin(admin.ModelAdmin):
    list_display = ("inventory_item", "brand", "model_number")

@admin.register(Stationery)
class StationeryAdmin(admin.ModelAdmin):
    list_display = ("inventory_item", "brand", "paper_size")


from django.contrib import admin
from .models import UniqueInventoryItem

@admin.register(UniqueInventoryItem)
class UniqueInventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity', 'unit_price', 'reorder_level', 'created_at', 'date_updated')
    search_fields = ('name', 'category')
    list_filter = ('category', 'department')
    ordering = ('-date_updated',)


from django.contrib import admin
from .models import InventoryItem, StockReceive, StockTransaction, InventoryTransaction


@admin.register(StockReceive)
class StockReceiveAdmin(admin.ModelAdmin):
    list_display = ("item", "quantity_received", "supplier", "received_by", "received_date", "status")
    search_fields = ("item__name", "supplier", "received_by__name")
    list_filter = ("status", "received_date")
    ordering = ("-received_date",)

@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ("transaction_type", "item", "quantity", "department", "transaction_by", "transaction_date")
    search_fields = ("item__name", "transaction_type", "department__name", "transaction_by__name")
    list_filter = ("transaction_type", "transaction_date")
    ordering = ("-transaction_date",)

@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ("transaction_type", "item", "quantity", "from_department", "to_department", "approved_by", "approved_at")
    search_fields = ("item__name", "transaction_type", "from_department__name", "to_department__name", "approved_by__name")
    list_filter = ("transaction_type", "approved_at")
    ordering = ("-approved_at",)
