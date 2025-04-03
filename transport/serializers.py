# from rest_framework import serializers
# from .models import Vehicle

# class VehicleSerializer(serializers.ModelSerializer):
#     vehicle_type = serializers.CharField(source='vehicle_type.type')  # Fetch vehicle type name
#     vehicle_image = serializers.SerializerMethodField()  # Format image URL

#     class Meta:
#         model = Vehicle
#         fields = [
#             "id", "license_plate", "vehicle_type", "make", "model", 
#             "year", "status", "mfg_year_month", "date_of_registration", "vehicle_image"
#         ]

#     def get_vehicle_image(self, obj):
#         """Return the full URL for the vehicle image."""
#         if obj.vehicle_image:
#             request = self.context.get('request')
#             return request.build_absolute_uri(obj.vehicle_image.url)
#         return None  # If no image, return None
