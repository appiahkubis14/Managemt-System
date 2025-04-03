from django import forms
from .models import InventoryItem,UniqueInventoryItem

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = UniqueInventoryItem
        fields = ['name', 'category', 'quantity', 'description', 'reorder_level', 'department']


from django import forms
from .models import InventoryRequest

class InventoryRequestForm(forms.ModelForm):
    class Meta:
        model = InventoryRequest
        fields = ['item', 'transaction_type', 'quantity', 'from_department', 'to_department', 'employee', 'remarks']
