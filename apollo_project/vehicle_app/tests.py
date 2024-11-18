from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Vehicle


class VehicleAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vehicle_data = {
            "vin": "1HGCM82633A123456",
            "manufacturer_name": "Honda",
            "description": "A reliable sedan.",
            "horse_power": 150,
            "model_name": "Accord",
            "model_year": 2022,
            "purchase_price": 22000.00,
            "fuel_type": "Gasoline"
        }
        self.vehicle = Vehicle.objects.create(**self.vehicle_data)

    def test_get_all_vehicles(self):
        response = self.client.get(reverse('vehicle-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_vehicle(self):
        new_vehicle = {
            "vin": "5NPE24AF3FH123457",
            "manufacturer_name": "Hyundai",
            "description": "A mid-size sedan.",
            "horse_power": 185,
            "model_name": "Sonata",
            "model_year": 2015,
            "purchase_price": 18000.00,
            "fuel_type": "Gasoline"
        }
        response = self.client.post(reverse('vehicle-list-create'), new_vehicle, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_vehicle_by_vin(self):
        response = self.client.get(reverse('vehicle-detail', args=[self.vehicle.vin]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_vehicle(self):
        update_data = {"horse_power": 155}
        response = self.client.put(reverse('vehicle-detail', args=[self.vehicle.vin]), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vehicle.refresh_from_db()
        self.assertEqual(self.vehicle.horse_power, 155)

    def test_delete_vehicle(self):
        response = self.client.delete(reverse('vehicle-detail', args=[self.vehicle.vin]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_vehicle_invalid_vin(self):
        invalid_vehicle = {
            "vin": "123",  # Invalid VIN (should be 17 characters)
            "manufacturer_name": "Toyota",
            "description": "Invalid VIN test.",
            "horse_power": 150,
            "model_name": "Corolla",
            "model_year": 2023,
            "purchase_price": 20000.00,
            "fuel_type": "Gasoline"
        }
        response = self.client.post(reverse('vehicle-list-create'), invalid_vehicle, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn("vin", response.data["errors"])

    def test_create_vehicle_missing_fields(self):
        incomplete_vehicle = {
            "vin": "1HGCM82633A123457",
            "manufacturer_name": "Honda"  # Missing other fields
        }
        response = self.client.post(reverse('vehicle-list-create'), incomplete_vehicle, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn("description", response.data["errors"])
        self.assertIn("horse_power", response.data["errors"])

    def test_create_vehicle_negative_purchase_price(self):
        invalid_vehicle = {
            "vin": "1HGCM82633A123458",
            "manufacturer_name": "Toyota",
            "description": "Negative purchase price test.",
            "horse_power": 150,
            "model_name": "Corolla",
            "model_year": 2023,
            "purchase_price": -10000.00,  # Invalid negative price
            "fuel_type": "Gasoline"
        }
        response = self.client.post(reverse('vehicle-list-create'), invalid_vehicle, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn("purchase_price", response.data["errors"])

    def test_update_vehicle_partial_data(self):
        update_data = {"description": "Updated description only."}
        response = self.client.put(reverse('vehicle-detail', args=[self.vehicle.vin]), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vehicle.refresh_from_db()
        self.assertEqual(self.vehicle.description, "Updated description only.")

    def test_delete_nonexistent_vehicle(self):
        nonexistent_vin = "1HGCM82633A000000"  # VIN not in database
        response = self.client.delete(reverse('vehicle-detail', args=[nonexistent_vin]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_vehicle_by_invalid_vin(self):
        invalid_vin = "1HGCM82633A000000"  # VIN not in database
        response = self.client.get(reverse('vehicle-detail', args=[invalid_vin]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_vehicles_empty_database(self):
        # Clear the database
        Vehicle.objects.all().delete()
        response = self.client.get(reverse('vehicle-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # Should return an empty list

    def test_create_vehicle_duplicate_vin(self):
        duplicate_vehicle = {
            "vin": self.vehicle.vin,  # Same VIN as the one created in setUp
            "manufacturer_name": "Toyota",
            "description": "Duplicate VIN test.",
            "horse_power": 180,
            "model_name": "Camry",
            "model_year": 2023,
            "purchase_price": 25000.00,
            "fuel_type": "Gasoline"
        }
        response = self.client.post(reverse('vehicle-list-create'), duplicate_vehicle, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn("vin", response.data["errors"])

    def test_create_vehicle_invalid_horse_power(self):
        invalid_vehicle = {
            "vin": "1HGCM82633A123459",
            "manufacturer_name": "Toyota",
            "description": "Horsepower should be numeric.",
            "horse_power": "one-fifty",  # Invalid string instead of a number
            "model_name": "Camry",
            "model_year": 2023,
            "purchase_price": 25000.00,
            "fuel_type": "Gasoline"
        }
        response = self.client.post(reverse('vehicle-list-create'), invalid_vehicle, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn("horse_power", response.data["errors"])

    def test_create_vehicle_invalid_fuel_type(self):
        invalid_vehicle = {
            "vin": "1HGCM82633A123460",
            "manufacturer_name": "Tesla",
            "description": "Invalid fuel type.",
            "horse_power": 300,
            "model_name": "Model 3",
            "model_year": 2023,
            "purchase_price": 45000.00,
            "fuel_type": "Water"  # Invalid fuel type
        }
        response = self.client.post(reverse('vehicle-list-create'), invalid_vehicle, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn("fuel_type", response.data["errors"])

    def test_create_vehicle_future_model_year(self):
        invalid_vehicle = {
            "vin": "1HGCM82633A123461",
            "manufacturer_name": "Honda",
            "description": "Model year cannot be too far in the future.",
            "horse_power": 180,
            "model_name": "Accord",
            "model_year": 3000,  # Invalid year
            "purchase_price": 25000.00,
            "fuel_type": "Gasoline"
        }
        response = self.client.post(reverse('vehicle-list-create'), invalid_vehicle, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn("model_year", response.data["errors"])

    def test_update_vehicle_invalid_vin(self):
        invalid_update_data = {"vin": "123"}  # Invalid VIN length
        response = self.client.put(reverse('vehicle-detail', args=[self.vehicle.vin]), invalid_update_data,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn("vin", response.data["errors"])

    def test_delete_vehicle_confirm_nonexistence(self):
        response = self.client.delete(reverse('vehicle-detail', args=[self.vehicle.vin]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Confirm the vehicle is no longer in the database
        response = self.client.get(reverse('vehicle-detail', args=[self.vehicle.vin]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_vehicle_long_description(self):
        long_description = "This is a very long description." * 50  # Long description
        valid_vehicle = {
            "vin": "1HGCM82633A123462",
            "manufacturer_name": "Ford",
            "description": long_description,
            "horse_power": 250,
            "model_name": "F-150",
            "model_year": 2023,
            "purchase_price": 35000.00,
            "fuel_type": "Gasoline"
        }
        response = self.client.post(reverse('vehicle-list-create'), valid_vehicle, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["description"], long_description)

    def test_create_vehicle_edge_case_year(self):
        oldest_vehicle = {
            "vin": "1HGCM82633A123463",
            "manufacturer_name": "Benz",
            "description": "The oldest car ever made.",
            "horse_power": 2,
            "model_name": "Motorwagen",
            "model_year": 1886,  # Earliest possible model year
            "purchase_price": 5000.00,
            "fuel_type": "Gasoline"
        }
        response = self.client.post(reverse('vehicle-list-create'), oldest_vehicle, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        next_year_vehicle = {
            "vin": "1HGCM82633A123464",
            "manufacturer_name": "Future Cars Inc.",
            "description": "Next year’s futuristic car.",
            "horse_power": 400,
            "model_name": "Futurista",
            "model_year": 2024,  # Assume the current year is 2023
            "purchase_price": 100000.00,
            "fuel_type": "Electric"
        }
        response = self.client.post(reverse('vehicle-list-create'), next_year_vehicle, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)