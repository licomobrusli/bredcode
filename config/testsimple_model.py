from django.test import TestCase
from config.models import SimpleModel  # Replace 'yourapp' with the actual name of your Django app
from .submit_order import create_entry_in_simple_model  # Adjust path as needed

class SimpleModelTest(TestCase):

    def test_create_entry_in_simple_model(self):
        # Call the function under test
        new_entry = create_entry_in_simple_model()

        # Ensure the entry was created correctly
        self.assertIsNotNone(new_entry.id, "The new SimpleModel entry should have a non-null id after creation.")
        self.assertEqual(new_entry.code, '1', "The new SimpleModel entry should have a code of '1'.")

        # Verify that the entry is indeed saved in the database
        saved_entry = SimpleModel.objects.get(id=new_entry.id)
        self.assertEqual(saved_entry.code, '1', "The SimpleModel entry saved in the database should have a code of '1'.")
