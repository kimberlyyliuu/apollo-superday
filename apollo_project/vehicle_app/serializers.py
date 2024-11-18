from rest_framework import serializers
from .models import Vehicle

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'  # Include all fields in the JSON output

    def validate_vin(self, value):
        """Ensure VIN is exactly 17 characters."""
        if len(value) != 17:
            raise serializers.ValidationError("VIN must be exactly 17 characters long.")
        return value

    def validate_purchase_price(self, value):
        """Ensure purchase price is a positive number."""
        if value <= 0:
            raise serializers.ValidationError("Purchase price must be greater than 0.")
        return value

    def validate_model_year(self, value):
        """Ensure model year is within a reasonable range."""
        if value < 1886 or value > 2100:
            raise serializers.ValidationError("Model year must be between 1886 and 2100.")
        return value

    def validate(self, data):
        """Ensure no fields are null or empty."""
        for field, value in data.items():
            if value is None or (isinstance(value, str) and value.strip() == ""):
                raise serializers.ValidationError({field: f"{field} cannot be null or empty."})
        return data

    ALLOWED_FUEL_TYPES = ["Gasoline", "Diesel", "Electric", "Hybrid"]

    def validate_fuel_type(self, value):
        """Validate that fuel_type is one of the allowed values."""
        if value not in self.ALLOWED_FUEL_TYPES:
            raise serializers.ValidationError(
                f"Invalid fuel type '{value}'. Allowed values are: {', '.join(self.ALLOWED_FUEL_TYPES)}."
            )
        return value