# tests.py
from django.test import TestCase
from config.models import (TimeResourcesQueue, ResourceModel, ModalCount, Segment, SegmentParam, ResourceType, ResourceAvailability, TimeResourceItems, ServiceCategory, Services)
from datetime import timedelta
from prettytable import PrettyTable
from config.time_utils import now_minutes

class TimeResourcesQueueSignalTest(TestCase):
    def setUp(self):
        # Create a ResourceType instance
        resource_type = ResourceType.objects.create(
            code='T',
            name='Test Resource Type',
            measure='Unit',
            unit_size=1
        )

        # Create ResourceModel instance
        resource_model = ResourceModel.objects.create(
            code='BARB',
            name='Test Resource Model',
            cost_per_unit=10.0,
            no_of_units=5,
            fungible=True,
            type=resource_type
        )

        # Create SegmentParam instances and assign them to instance variables
        self.container_segment_param = SegmentParam.objects.create(
            code='CTNT',
            name='Container Segment',
            container=True,
            calc_available=1
        )
        self.non_container_segment_param = SegmentParam.objects.create(
            code='NCSP',
            name='Non-Container Segment',
            container=False,
            calc_available=-1
        )

        # Define the start and end times for container and lunch segments
        today = now_minutes().replace(hour=0, minute=0, second=0, microsecond=0)
        container_start = today.replace(hour=10)
        container_end = today.replace(hour=22)

         # Create TimeResourceItems instance
        self.time_resource_item = TimeResourceItems.objects.create(
            resource_item_code='pmontoya',
            name='Pablo Montoya',
            description='This is Pablo he is a barber',
            start_date=today.date(),
            resource_model=resource_model,
        )

        segment_instance = Segment.objects.create(
            code='SHFT', 
            type='SC', 
            segment_param=self.container_segment_param
        )

        # Create container TimeResourcesQueue instance using container_segment_param
        self.container_trq = TimeResourcesQueue.objects.create(
            resource_item_code=self.time_resource_item,
            segment=segment_instance,
            segment_start=container_start,
            segment_end=container_end,
            resource_model=resource_model,
            segment_params=self.container_segment_param
        )

        # Create ServiceCategory and Services instances
        self.service_category = ServiceCategory.objects.create(
            code='SC01',
            name='Service Category',
            description='Test Service Category'
        )
        
        self.service = Services.objects.create(
            code='SV01',
            name='Service',
            service_category=self.service_category,
            description='Test Service',
            total_duration=30,
            price=50.00
        )
        
        self.modal_count_shampoo = ModalCount.objects.create(
            code=segment_instance,  # Use the Segment instance here
            name='Shampoo', 
            description='Shampoo Description', 
            duration=5, 
            price=100.00, 
            max_quantity=10, 
            category_code=self.service_category, 
            service_code=self.service
        )

    def test_post_delete_signal(self):
        today = now_minutes().replace(hour=0, minute=0, second=0, microsecond=0)
        # Check the initial state before adding lunch
        remaining_trqs = TimeResourcesQueue.objects.all()
        self.assertEqual(remaining_trqs.count(), 1)
        self.assertEqual(remaining_trqs.first(), self.container_trq)

        # Use the TimeResourceItems instance for filtering ResourceAvailability
        availability_segments = ResourceAvailability.objects.filter(resource_item=self.time_resource_item).order_by('available_start')
        self.assertEqual(availability_segments.count(), 1)

        # Create lunch TimeResourcesQueue instance using non_container_segment_param
        lunch_start = now_minutes().replace(hour=15, minute=0)
        lunch_end = now_minutes().replace(hour=16, minute=0)
        lunch_segment = Segment.objects.create(
            code='LNCH',  # A unique code for the lunch segment
            type='Break',  # Assuming 'Break' is a valid type for this example
            segment_param=self.non_container_segment_param
        )

        lunch_trq = TimeResourcesQueue.objects.create(
            resource_item_code=self.time_resource_item,
            segment=lunch_segment,  # Use the newly created Segment instance
            segment_start=lunch_start,
            segment_end=lunch_end,
            resource_model=self.container_trq.resource_model,
            segment_params=self.non_container_segment_param
        )

        # Check the state after adding lunch
        remaining_trqs = TimeResourcesQueue.objects.all()
        self.assertEqual(remaining_trqs.count(), 2)

        # create task TimeResourcesQueue instance using non_container_segment_param
        task_start = now_minutes().replace(hour=16, minute=30)
        task_end = now_minutes().replace(hour=17, minute=0)
        self.task_segment = Segment.objects.create(
            code='TST',  # A unique code for the task segment
            type='Task',  # Assuming 'Task' is a valid type for this example
            segment_param=self.non_container_segment_param
        )

        TimeResourcesQueue.objects.create(
            resource_item_code=self.time_resource_item,
            segment=self.task_segment,  # Use the newly created Segment instance
            segment_start=task_start,
            segment_end=task_end,
            resource_model=self.container_trq.resource_model,
            segment_params=self.non_container_segment_param
        )

        # Create second task TimeResourcesQueue instance immediately following the first
        task_trq2_start = task_end
        task_trq2_end = task_end + timedelta(minutes=10)
        TimeResourcesQueue.objects.create(
            resource_item_code=self.time_resource_item,
            segment=self.task_segment,  # Reusing the same segment type for simplicity
            segment_start=task_trq2_start,
            segment_end=task_trq2_end,
            resource_model=self.container_trq.resource_model,
            segment_params=self.non_container_segment_param
        )

        # Assert the state after adding back-to-back task segments
        remaining_trqs = TimeResourcesQueue.objects.all()
        self.assertEqual(remaining_trqs.count(), 4)  # Expecting 4 TRQs: container, lunch, task1, task2

        # here i need to see everything that is in the time resource queue in a pretty table
        trqs = TimeResourcesQueue.objects.all()
        table = PrettyTable()
        table.field_names = ["Resource Item", "Segment", "Start", "End"]
        for trq in trqs:
            table.add_row([trq.resource_item_code, trq.segment, trq.segment_start, trq.segment_end])
        print(table)

        # here i need to see everything that is in the resource availability in a pretty table
        availability_segments = ResourceAvailability.objects.filter(resource_item=self.time_resource_item).order_by('available_start')
        table = PrettyTable()
        table.field_names = ["Start", "End"]
        for segment in availability_segments:
            table.add_row([segment.available_start, segment.available_end])
        print(table)

       # Corrected Assertions for TimeResourcesQueue
        expected_trqs = [
            ('pmontoya', 'SHFT - SC', today.strftime('%Y-%m-%d') + ' 10:00:00+0000', today.strftime('%Y-%m-%d') + ' 22:00:00+0000'),
            ('pmontoya', 'LNCH - Break', today.strftime('%Y-%m-%d') + ' 15:00:00+0000', today.strftime('%Y-%m-%d') + ' 16:00:00+0000'),
            ('pmontoya', 'TST - Task', today.strftime('%Y-%m-%d') + ' 16:30:00+0000', today.strftime('%Y-%m-%d') + ' 17:00:00+0000'),
            ('pmontoya', 'TST - Task', today.strftime('%Y-%m-%d') + ' 17:00:00+0000', today.strftime('%Y-%m-%d') + ' 17:10:00+0000')
        ]

        for trq, (code, seg, start, end) in zip(TimeResourcesQueue.objects.order_by('segment_start'), expected_trqs):
            self.assertEqual(trq.resource_item_code.resource_item_code, code)
            self.assertEqual(f'{trq.segment.code} - {trq.segment.type}', seg)
            self.assertEqual(trq.segment_start.strftime("%Y-%m-%d %H:%M:%S%z"), start)
            self.assertEqual(trq.segment_end.strftime("%Y-%m-%d %H:%M:%S%z"), end)

        # Assertions for ResourceAvailability
        expected_availability = [
            (today.strftime('%Y-%m-%d') + ' 10:00:00+0000', today.strftime('%Y-%m-%d') + ' 15:00:00+0000'),
            (today.strftime('%Y-%m-%d') + ' 16:00:00+0000', today.strftime('%Y-%m-%d') + ' 16:30:00+0000'),
            (today.strftime('%Y-%m-%d') + ' 17:10:00+0000', today.strftime('%Y-%m-%d') + ' 22:00:00+0000')
        ]

        for availability, (start, end) in zip(ResourceAvailability.objects.filter(resource_item=self.time_resource_item).order_by('available_start'), expected_availability):
            self.assertEqual(availability.available_start.strftime('%Y-%m-%d %H:%M:%S%z'), start)
            self.assertEqual(availability.available_end.strftime('%Y-%m-%d %H:%M:%S%z'), end)
