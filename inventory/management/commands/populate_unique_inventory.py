from django.core.management.base import BaseCommand
from inventory.models import InventoryItem, UniqueInventoryItem

class Command(BaseCommand):
    help = 'Populate the UniqueInventoryItem model with combined inventory data'

    def handle(self, *args, **kwargs):
        # Fetch all inventory items
        inventory_items = InventoryItem.objects.all()

        # Create a dictionary to store unique items
        unique_items = {}

        for item in inventory_items:
            item_key = (item.name, item.category, item.unit_price)  # Combining fields that should be unique
            if item_key in unique_items:
                unique_items[item_key]['quantity'] += item.quantity
                # You may want to decide how to handle reorder_level (e.g., keep the lowest, highest, or average)
                unique_items[item_key]['reorder_level'] = min(
                    unique_items[item_key]['reorder_level'], item.reorder_level
                )
            else:
                unique_items[item_key] = {
                    'name': item.name,
                    'category': item.category,
                    'quantity': item.quantity,
                    'unit_price': item.unit_price,
                    'description': item.description,
                    'created_at': item.created_at,
                    'reorder_level': item.reorder_level,  # Add reorder level to the dictionary
                }

        # Now save or update the UniqueInventoryItem model
        for item_key, item_data in unique_items.items():
            UniqueInventoryItem.objects.update_or_create(
                name=item_data['name'],
                category=item_data['category'],
                unit_price=item_data['unit_price'],
                defaults={
                    'quantity': item_data['quantity'],
                    'description': item_data['description'],
                    'created_at': item_data['created_at'],
                    'reorder_level': item_data['reorder_level'],  # Add reorder level in the update
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the UniqueInventoryItem model'))
