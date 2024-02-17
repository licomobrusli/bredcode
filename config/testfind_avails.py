# testfind_avails.py
from django.utils import timezone
from datetime import timedelta
from django.test import TestCase
from config.models import ResourceAvailability, ResourceModel, ResourceType, TimeResourceItems
from config.submit_order import find_earliest_availability

class FindEarliestAvailabilityTestCase(TestCase):
    def setUp(self):
        # Set up test data
        self.resource_type = ResourceType.objects.create(
            code='T',
            name='Time Resource',
            measure='Time',
            unit_size=1
        )
        self.resource_model = ResourceModel.objects.create(
            code='RM001',
            name='Test Resource Model',
            type=self.resource_type,
            cost_per_unit=10.00,
            no_of_units=1,
            fungible=False
        )
        # Ensure to create a TimeResourceItems instance since ResourceAvailability expects a non-null resource_item
        self.time_resource_item = TimeResourceItems.objects.create(
            resource_item_code='TRI001',
            name='Test Time Resource Item',
            description='Test Description',
            resource_model=self.resource_model,
            start_date=timezone.now().replace(microsecond=0).date(),  # Adjust as necessary
            # Add other fields if necessary
        )
        self.start_time = timezone.now().replace(microsecond=0)
        self.end_time = self.start_time + timedelta(hours=3)
        self.resource_availability = ResourceAvailability.objects.create(
            resource_item=self.time_resource_item,
            resource_model=self.resource_model,
            available_start=self.start_time,
            available_end=self.end_time,
            duration=timedelta(hours=3)  # Adjust based on your logic
        )

    def test_find_earliest_availability_within_available_time(self):
        # Test finding availability within the set-up time range
        phase_duration = 60  # Duration in minutes
        expected_start_time = self.start_time
        expected_end_time = expected_start_time + timedelta(minutes=phase_duration)

        start_time, end_time, resource_item = find_earliest_availability(
            self.resource_model.code, phase_duration
        )

        self.assertEqual(start_time, expected_start_time)
        self.assertEqual(end_time, expected_end_time)
        self.assertEqual(resource_item, self.time_resource_item)

    def test_no_availability(self):
        # Test when there is no availability at all
        ResourceAvailability.objects.all().delete()  # Remove all availabilities

        phase_duration = 60  # Duration in minutes

        start_time, end_time, resource_item = find_earliest_availability(
            self.resource_model.code, phase_duration
        )

        # Expect no availability
        self.assertIsNone(start_time)
        self.assertIsNone(end_time)
        self.assertIsNone(resource_item)

    def test_find_earliest_availability_starts_in_future(self):
        # Set the resource to become available in 1 hour from now for 3 hours
        future_start_time = timezone.now().replace(microsecond=0) + timedelta(hours=1)
        future_end_time = future_start_time + timedelta(hours=3)  # Adjust based on your logic

        # Update the resource availability to reflect this new availability window
        self.resource_availability.available_start = future_start_time
        self.resource_availability.available_end = future_end_time
        self.resource_availability.save()

        # Duration of the phase we are testing for
        phase_duration = 60  # Duration in minutes
        # Expected start time would be one hour from now, as that's when the resource becomes available
        expected_start_time = future_start_time
        # Expected end time would be one hour and the phase duration from now
        expected_end_time = expected_start_time + timedelta(minutes=phase_duration)

        # Run find_earliest_availability with the updated availability
        start_time, end_time, resource_item = find_earliest_availability(
            self.resource_model.code, phase_duration
        )

        # Assert that the function finds the next available slot correctly, starting in one hour from now
        self.assertEqual(start_time, expected_start_time)
        self.assertEqual(end_time, expected_end_time)
        self.assertEqual(resource_item, self.time_resource_item)

    def test_find_earliest_availability_starts_in_past(self):
        # Set the resource to have been available 1 hour ago from now and still available for the next 2 hours
        past_start_time = timezone.now().replace(microsecond=0) - timedelta(hours=1)
        past_end_time = past_start_time + timedelta(hours=3)  # Adjust if needed; this should cover past to future

        # Update the resource availability to reflect this new availability window
        self.resource_availability.available_start = past_start_time
        self.resource_availability.available_end = past_end_time
        self.resource_availability.save()

        # Duration of the phase we are testing for
        phase_duration = 60  # Duration in minutes
        # Expected start time should match the time from one hour ago since it's still within the availability window
        expected_start_time = timezone.now().replace(microsecond=0)
        # Expected end time should be one hour after the expected start time based on the phase duration
        expected_end_time = expected_start_time + timedelta(minutes=phase_duration)

        # Run find_earliest_availability with the updated availability
        start_time, end_time, resource_item = find_earliest_availability(
            self.resource_model.code, phase_duration
        )

        # Assert that the function finds the available slot correctly, which started in the past and is still ongoing
        self.assertEqual(start_time, expected_start_time)
        self.assertEqual(end_time, expected_end_time)
        self.assertEqual(resource_item, self.time_resource_item)

    def test_availability_with_future_last_phase_end_time(self):
        # Availability starts now and lasts for 3 hours
        start_time_now = timezone.now().replace(microsecond=0)
        end_time_in_future = start_time_now + timedelta(hours=3)

        # Update the resource availability
        self.resource_availability.available_start = start_time_now
        self.resource_availability.available_end = end_time_in_future
        self.resource_availability.save()

        # Set the last phase end time to 1 hour in the future
        last_phase_end_time = start_time_now + timedelta(hours=1)

        # Duration of the phase we are testing for
        phase_duration = 60  # Duration in minutes
        # Expected start time should be one hour from now since last_phase_end_time is in the future
        expected_start_time = last_phase_end_time
        # Expected end time should be one hour after the expected start time
        expected_end_time = expected_start_time + timedelta(minutes=phase_duration)

        # Run find_earliest_availability with the last phase end time
        start_time, end_time, resource_item = find_earliest_availability(
            self.resource_model.code, phase_duration, last_phase_end_time
        )

        # Assert that the function finds the correct available slot after the last phase end time
        self.assertEqual(start_time, expected_start_time)
        self.assertEqual(end_time, expected_end_time)
        self.assertEqual(resource_item, self.time_resource_item)

    def test_phase_duration_longer_than_availability(self):
        # Set the resource to be available for 1 hour
        start_time = timezone.now().replace(microsecond=0)
        end_time = start_time + timedelta(hours=1)

        # Update the resource availability to reflect this new availability window
        self.resource_availability.available_start = start_time
        self.resource_availability.available_end = end_time
        self.resource_availability.save()

        # Duration of the phase we are testing for
        phase_duration = 120  # Duration in minutes; longer than the availability
        # Run find_earliest_availability with the updated availability
        start_time, end_time, resource_item = find_earliest_availability(
            self.resource_model.code, phase_duration
        )

        # Expect no availability since the phase duration is longer than the available time
        self.assertIsNone(start_time)
        print("TEST DEBUG")
        self.assertIsNone(end_time)
        self.assertIsNone(resource_item)