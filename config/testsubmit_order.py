# testsubmit_order.py
from datetime import timedelta
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import ServiceCategory, Services, ModalCount, Orders, OrderItems, Phase, PhaseResource, ResourceType, ResourceModel, Segment, SegmentParam, ResourceAvailability, TimeResourceItems, TimeResourcesQueue
from django.utils.timezone import now
from prettytable import PrettyTable
from config.time_utils import now_minutes

import logging
logger = logging.getLogger(__name__)

# the test set up should include the following:
    # 1. 2 barbers with different start times and the same end time
    # 2. 1 waiting chair for wiating phases with initial availability whilst open
    # 3. Lunches for each the barbers at the same time
    # 4. 3 services: wash, cut, color
    # 5. 3 phases for the wash service: shampoo, condition, blowdry
    # 6. 1 resource requirement for each phase of the wash service: a barber
    # 7. 1 phase for the cut service: cut
    # 8. 1 resource requirement for the cut phase: a barber
    # 9. 5 phases for the color service: prep, waitprep, color, waitcolor, rinse
    # 10. 2 resource requirements for the prep phase: 2 barbers
    # 11. 1 resource requirement for the color phase: 1 barber
    # 12. 1 resource requirement for the rinse phase: 1 barber
    # 13. 1 resource requirement for each wait phase: 1 waiting chairs


class OrderAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        segment_param_containers = SegmentParam.objects.create(
            code='CNTN',
            name='Containers Segment Params',
            description='A segment param for containers',
            container=True,
            contained=False,
            available=True,
            working=True,
            active=False,
            paid=True,
            calc_pay=1,
            calc_available=1
        )

        segment_param_unpaid_exceptions = SegmentParam.objects.create(
            code='UPEX',
            name='Unpaid Exception Segment Params',
            description='A segment param for unpaid exceptions',
            container=False,
            contained=True,
            available=False,
            working=False,
            active=False,
            paid=False,
            calc_pay=-1,
            calc_available=-1
        )

        segment_container_shift = Segment.objects.create(
            code='SHFT',
            type='SC',
            segment_param=segment_param_containers
        )

        segment_unpaid_ex_lunch = Segment.objects.create(
            code='LUNCH',
            type='SC',
            segment_param=segment_param_unpaid_exceptions
        )

        self.resource_type_time = ResourceType.objects.create(
            code='T', 
            name='Time', 
            measure='minute', 
            unit_size=1
        )

        self.resource_model_chair = ResourceModel.objects.create(
            code='CHAI', 
            name='A chair', 
            type=self.resource_type_time,
            cost_per_unit=0, 
            no_of_units=10, 
            fungible=True
        )

        self.resource_model_barber = ResourceModel.objects.create(
            code='BARB', 
            name='A barber', 
            type=self.resource_type_time,
            cost_per_unit=10, 
            no_of_units=10, 
            fungible=False
        )

        self.timeResourceItem_cher1 = TimeResourceItems.objects.create(
            resource_item_code='cher1',
            name='Cher 1',
            description='A test resource item for availability',
            resource_model=self.resource_model_chair
        )
        
        self.timeResourceItem_pmontoya = TimeResourceItems.objects.create(
            resource_item_code='pmontoya',
            name='Pablo Montoya',
            description='A test resource item for availability',
            resource_model=self.resource_model_barber
        )

        self.timeResourceItem_jdoe = TimeResourceItems.objects.create(
            resource_item_code='jdoe',
            name='John Doe',
            description='A test resource item for availability',
            resource_model=self.resource_model_barber
        )

        container_start = now_minutes() - timedelta(hours=1)
        container_end = now_minutes() + timedelta(hours=2)
        container_start2 = now_minutes() + timedelta(minutes=10)

        self.container_trq_cher1 = TimeResourcesQueue.objects.create(
            resource_item_code=self.timeResourceItem_cher1,
            segment=segment_container_shift,
            segment_start=container_start,
            segment_end=container_end,
            resource_model=self.resource_model_chair,
            segment_params=segment_param_containers
        )

        self.container_trq_pmontoya = TimeResourcesQueue.objects.create(
            resource_item_code=self.timeResourceItem_pmontoya,
            segment=segment_container_shift,
            segment_start=container_start,
            segment_end=container_end,
            resource_model=self.resource_model_barber,
            segment_params=segment_param_containers
        )

        self.container_trq_jdoe = TimeResourcesQueue.objects.create(
            resource_item_code=self.timeResourceItem_jdoe,
            segment=segment_container_shift,
            segment_start=container_start2,
            segment_end=container_end,
            resource_model=self.resource_model_barber,
            segment_params=segment_param_containers
        )

        lunch_start = now_minutes() + timedelta(hours=1)
        lunch_end = now_minutes() + timedelta(hours=1, minutes=10)

        self.lunch_trq_pmontoya = TimeResourcesQueue.objects.create(
            resource_item_code=self.timeResourceItem_pmontoya,
            segment=segment_unpaid_ex_lunch,
            segment_start=lunch_start,
            segment_end=lunch_end,
            resource_model=self.resource_model_barber,
            segment_params=segment_param_unpaid_exceptions
        )

        self.lunch_trq_jdoe = TimeResourcesQueue.objects.create(
            resource_item_code=self.timeResourceItem_jdoe,
            segment=segment_unpaid_ex_lunch,
            segment_start=lunch_start,
            segment_end=lunch_end,
            resource_model=self.resource_model_barber,
            segment_params=segment_param_unpaid_exceptions
        )

        self.segment_param_tasks = SegmentParam.objects.create(
            code='TASKS',
            name='Task Segment',
            description='A task segment param',
            container=False,
            contained=True,
            available=False,
            working=True,
            active=True,
            paid=True,
            calc_pay=0,
            calc_available='-1'
        )

        # Create Segment instance
        self.segment_task_wash = Segment.objects.create(
            code='WSH1',
            type='MC',
            segment_param=self.segment_param_tasks
        )
        
        # Set up category and services
        self.service_category_hed = ServiceCategory.objects.create(
            code='HED', 
            name='Head stuff', 
            description='Head Stuff Services'
        )
        
        self.service_wash = Services.objects.create(
            code='WSH', 
            name='Wash hair', 
            description='Basic hair wash', 
            total_duration=30,
            price=50, 
            service_category=self.service_category_hed
        )
        
        self.modal_count_wash = ModalCount.objects.create(
            code=self.segment_task_wash,
            name='Wash hair',
            description='Wash the hair yo',
            duration=30,
            price=10,
            max_quantity=10,
            category_code=self.service_category_hed,
            service_code=self.service_wash,
            logic='NOT',
            sub=0,
            sequence=1,
        )

        # Phases and resources setup for wash
        self.phase_shampoo = Phase.objects.create(
            code='WSH01', 
            name='Shampoo', 
            sequence=1, 
            duration=10,
            modal_count=self.modal_count_wash, 
        )
        
        self.phase_condition = Phase.objects.create(
            code='WSH02', 
            name='Condition', 
            sequence=2, 
            duration=10,
            modal_count=self.modal_count_wash, 
        )

        self.phase_blowdry = Phase.objects.create(
            code='WSH03', 
            name='Blowdry', 
            sequence=3, 
            duration=10,
            modal_count=self.modal_count_wash, 
        )

        self.phase_resource_shampoo = PhaseResource.objects.create(
            code='PRW01', 
            name='Barber to shampoo', 
            phase_code=self.phase_shampoo, 
            resource_models_code=self.resource_model_barber, 
            resource_types_code=self.resource_type_time
        )

        self.phase_resource_condition = PhaseResource.objects.create(
            code='PRW02', 
            name='Barber to condition', 
            phase_code=self.phase_condition, 
            resource_models_code=self.resource_model_barber, 
            resource_types_code=self.resource_type_time
        )

        self.phase_resource_blowdry = PhaseResource.objects.create(
            code='PRW03', 
            name='Barber to blowdry', 
            phase_code=self.phase_blowdry, 
            resource_models_code=self.resource_model_barber, 
            resource_types_code=self.resource_type_time
        )

        # now we will make all the required instances for a 2nd item: a haircut
        self.segment_task_cut = Segment.objects.create(
            code='CUT1',
            type='MC',
            segment_param=self.segment_param_tasks
        )

        self.service_cut = Services.objects.create(
            code='CUT', 
            name='Cut hair', 
            description='Basic hair cut', 
            total_duration=30,
            price=50, 
            service_category=self.service_category_hed
        )

        self.modal_count_cut = ModalCount.objects.create(
            code=self.segment_task_cut,
            name='Cut hair',
            description='Cut the hair yo',
            duration=30,
            price=10,
            max_quantity=10,
            category_code=self.service_category_hed,
            service_code=self.service_cut,
            logic='NOT',
            sub=0,
            sequence=1,
        )

        self.phase_cut = Phase.objects.create(
            code='CUT01', 
            name='Cut', 
            sequence=1, 
            duration=30,
            modal_count=self.modal_count_cut, 
        )

        self.phase_resource_cut = PhaseResource.objects.create(
            code='PRC01', 
            name='Barber to cut', 
            phase_code=self.phase_cut, 
            resource_models_code=self.resource_model_barber, 
            resource_types_code=self.resource_type_time
        )

        # now we will make all the required instances for a 3rd item: a color
        self.segment_task_color = Segment.objects.create(
            code='CLR1',
            type='MC',
            segment_param=self.segment_param_tasks
        )

        self.service_color = Services.objects.create(
            code='CLR', 
            name='Color hair', 
            description='Basic hair color', 
            total_duration=30,
            price=50, 
            service_category=self.service_category_hed
        )

        self.modal_count_color = ModalCount.objects.create(
            code=self.segment_task_color,
            name='Color hair',
            description='Color the hair yo',
            duration=30,
            price=10,
            max_quantity=10,
            category_code=self.service_category_hed,
            service_code=self.service_color,
            logic='NOT',
            sub=0,
            sequence=1,
        )

        self.phase_prep = Phase.objects.create(
            code='CLR01', 
            name='Prep', 
            sequence=1, 
            duration=10,
            modal_count=self.modal_count_color, 
        )

        self.phase_waitprep = Phase.objects.create(
            code='CLR02', 
            name='Wait for prep', 
            sequence=2, 
            duration=10,
            modal_count=self.modal_count_color, 
        )

        self.phase_color = Phase.objects.create(
            code='CLR03', 
            name='Color', 
            sequence=3, 
            duration=10,
            modal_count=self.modal_count_color, 
        )

        self.phase_waitcolor = Phase.objects.create(
            code='CLR04', 
            name='Wait for color', 
            sequence=4, 
            duration=10,
            modal_count=self.modal_count_color, 
        )

        self.phase_rinse = Phase.objects.create(
            code='CLR05', 
            name='Rinse', 
            sequence=5, 
            duration=10,
            modal_count=self.modal_count_color, 
        )

        self.phase_resource1_prep = PhaseResource.objects.create(
            code='PPC01', 
            name='Barber to prep', 
            phase_code=self.phase_prep, 
            resource_models_code=self.resource_model_barber, 
            resource_types_code=self.resource_type_time
        )
        
        self.phase_resource2_prep = PhaseResource.objects.create(
            code='PRC99', 
            name='Barber to prep', 
            phase_code=self.phase_prep, 
            resource_models_code=self.resource_model_barber, 
            resource_types_code=self.resource_type_time
        )

        self.phase_resource_waitprep = PhaseResource.objects.create(
            code='PRC02', 
            name='Waiting chair for prep', 
            phase_code=self.phase_waitprep, 
            resource_models_code=self.resource_model_chair, 
            resource_types_code=self.resource_type_time
        )

        self.phase_resource_color = PhaseResource.objects.create(
            code='PRC03', 
            name='Barber to color', 
            phase_code=self.phase_color, 
            resource_models_code=self.resource_model_barber, 
            resource_types_code=self.resource_type_time
        )

        self.phase_resource_waitcolor = PhaseResource.objects.create(
            code='PRC04', 
            name='Waiting chair for color', 
            phase_code=self.phase_waitcolor, 
            resource_models_code=self.resource_model_chair, 
            resource_types_code=self.resource_type_time
        )

        self.phase_resource_rinse = PhaseResource.objects.create(
            code='PRC05', 
            name='Barber to rinse', 
            phase_code=self.phase_rinse, 
            resource_models_code=self.resource_model_barber, 
            resource_types_code=self.resource_type_time
        )


    def display_time_resources_queue(self):
        trqs = TimeResourcesQueue.objects.all().order_by('resource_item_code', 'segment_start')
        table = PrettyTable()
        table.field_names = ["Resource Item Code", "Segment", "Start Time", "End Time", "Resource Model"]
        for trq in trqs:
            table.add_row([trq.resource_item_code, trq.segment, trq.segment_start, trq.segment_end, trq.resource_model])
        print("Time Resources Queue Table:")
        print(table)

    def display_resource_availability(self):
        resource_availabilities = ResourceAvailability.objects.all().order_by('resource_item', 'available_start')
        table = PrettyTable()
        table.field_names = ["Resource Item", "Resource Model", "Available Start", "Available End", "Duration"]
        for ra in resource_availabilities:
            table.add_row([ra.resource_item, ra.resource_model, ra.available_start, ra.available_end, ra.duration])
        print("Resource Availability Table:")
        print(table)

    def test_create_order_and_order_items(self):
        # Arrange

        self.assertEqual(Orders.objects.count(), 0, "Orders should have 0 after setup.")
        self.assertEqual(OrderItems.objects.count(), 0, "OrderItems should have 0 after setup.")
        self.assertEqual(TimeResourcesQueue.objects.filter(resource_item_code=self.timeResourceItem_pmontoya).count(), 2, "2 trq for pmontoya 1 container 1 lunch")
        self.assertEqual(TimeResourcesQueue.objects.filter(resource_item_code=self.timeResourceItem_jdoe).count(), 2, "2 trq for jdoe 1 container 1 lunch")
        self.assertEqual(TimeResourcesQueue.objects.filter(resource_item_code=self.timeResourceItem_cher1).count(), 1, "1 trq for chair")
        self.assertEqual(TimeResourcesQueue.objects.count(), 5, "TimeResourcesQueue should have 5 after setup.")

        self.assertEqual(ResourceAvailability.objects.filter(resource_model=self.resource_model_barber).count(), 4, "4 ResourceAvailability for barber")
        self.assertEqual(ResourceAvailability.objects.filter(resource_item=self.timeResourceItem_pmontoya).count(), 2, "2 ResourceAvailability for pmontoya")
        self.assertEqual(ResourceAvailability.objects.filter(resource_item=self.timeResourceItem_jdoe).count(), 2, "2 ResourceAvailability for jdoe")
        self.assertEqual(ResourceAvailability.objects.filter(resource_model=self.resource_model_chair).count(), 1, "1 ResourceAvailability for chair")
        self.assertEqual(ResourceAvailability.objects.filter(resource_item=self.timeResourceItem_cher1).count(), 1, "1 ResourceAvailability for cher1")
        self.assertEqual(ResourceAvailability.objects.count(), 5, "ResourceAvailability should have 5 after setup.")
                         
        url = '/api/submit_order/'
        first_order_data = {
            'order': {
                'item_count': 3,  # Updated to reflect the total number of service items
                'order_price': 70.00,  # Updated total order price, adjust based on actual prices
                'order_number': 'ORD123456'
            },
            'items': [
                {
                    'modal_count': self.segment_task_wash.code,
                    'item_name': 'wash hair',
                    'unit_price': 10,
                    'item_count': 1,
                    'item_price': 10,
                },
                {
                    'modal_count': self.segment_task_cut.code,
                    'item_name': 'Cut hair',
                    'unit_price': 20,  # Adjust based on actual price
                    'item_count': 1,
                    'item_price': 20,
                },
                {
                    'modal_count': self.segment_task_color.code,
                    'item_name': 'Color hair',
                    'unit_price': 40,  # Adjust based on actual price
                    'item_count': 1,
                    'item_price': 40,
                }
            ]
        }

        # Submit the first order
        first_response = self.client.post(url, first_order_data, format='json')
        self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)

        # Second order - Same as the first with different order number
        second_order_data = {
            'order': {
                'item_count': 3,  # Reflects the total number of service items
                'order_price': 70.00,  # Total order price
                'order_number': 'ORD123457'  # New order number
            },
            'items': [
                {
                    'modal_count': self.segment_task_wash.code,
                    'item_name': 'Wash hair',
                    'unit_price': 10,
                    'item_count': 1,
                    'item_price': 10,
                },
                {
                    'modal_count': self.segment_task_cut.code,
                    'item_name': 'Cut hair',
                    'unit_price': 20,  # Actual price
                    'item_count': 1,
                    'item_price': 20,
                },
                {
                    'modal_count': self.segment_task_color.code,
                    'item_name': 'Color hair',
                    'unit_price': 40,  # Actual price
                    'item_count': 1,
                    'item_price': 40,
                }
            ]
        }

        # Submit the second order
        second_response = self.client.post(url, second_order_data, format='json')
        self.assertEqual(second_response.status_code, status.HTTP_201_CREATED)

        # Third order - Only includes a haircut
        third_order_data = {
            'order': {
                'item_count': 1,  # Only one service item
                'order_price': 20.00,  # Price for the haircut only
                'order_number': 'ORD123458'  # New order number
            },
            'items': [
                {
                    'modal_count': self.segment_task_cut.code,
                    'item_name': 'Cut hair',
                    'unit_price': 20,  # Actual price for a haircut
                    'item_count': 1,
                    'item_price': 20,
                }
            ]
        }

        # Submit the third order
        third_response = self.client.post(url, third_order_data, format='json')
        self.assertEqual(third_response.status_code, status.HTTP_201_CREATED)

        # output the pretty tables for the TimeResourcesQueue and ResourceAvailability
        self.display_time_resources_queue()
        self.display_resource_availability()

        # log all trq instances
        logger.debug(TimeResourcesQueue.objects.all())
        # log all resource availability instances
        logger.debug(ResourceAvailability.objects.all())

        # # Assert
        # self.assertEqual(Orders.objects.count(), 3, "Orders should have 3 after adding 3.")
        # self.assertEqual(OrderItems.objects.count(), 7, "OrderItems should have 7 after adding 7.")
        # self.assertEqual(TimeResourcesQueue.objects.count(), 15, "TimeResourcesQueue should have 15 after adding 15.")
        # self.assertEqual(TimeResourcesQueue.objects.filter(
        #     resource_item_code=self.timeResourceItem_pmontoya,
        #     segment=self.segment_task_wash,
        #     resource_model=self.resource_model_barber
        # ).count(), 3, "TimeResourcesQueue should have 3 for Pablo Montoya after adding 3.")
        # self.assertEqual(TimeResourcesQueue.objects.filter(
        #     resource_item_code=self.timeResourceItem_jdoe,
        #     segment=self.segment_task_wash,
        #     resource_model=self.resource_model_barber
        # ).count(), 3, "TimeResourcesQueue should have 3 for John Doe after adding 3.")
        # self.assertEqual(TimeResourcesQueue.objects.filter(
        #     resource_item_code=self.timeResourceItem_pmontoya,
        #     segment=self.segment_task_cut,
        #     resource_model=self.resource_model_barber
        # ).count(), 3, "TimeResourcesQueue should have 3 for Pablo Montoya after adding 3.")
        # self.assertEqual(TimeResourcesQueue.objects.filter(
        #     resource_item_code=self.timeResourceItem_jdoe,
        #     segment=self.segment_task_cut,
        #     resource_model=self.resource_model_barber
        # ).count(), 3, "TimeResourcesQueue should have 3 for John Doe after adding 3.")
        # self.assertEqual(TimeResourcesQueue.objects.filter(
        #     resource_item_code=self.timeResourceItem_pmontoya,
        #     segment=self.segment_task_color,
        #     resource_model=self.resource_model_barber
        # ).count(), 3, "TimeResourcesQueue should have 3 for Pablo Montoya after adding 3.")
        # self.assertEqual(TimeResourcesQueue.objects.filter(
        #     resource_item_code=self.timeResourceItem_jdoe,
        #     segment=self.segment_task_color,
        #     resource_model=self.resource_model_barber
        # ).count(), 3, "TimeResourcesQueue should have 3 for John Doe after adding 3.")
        # self.assertEqual(TimeResourcesQueue.objects.filter(
        #     resource_item_code=self.timeResourceItem_cher1,
        #     segment=self.segment_task_color,
        #     resource_model=self.resource_model_chair
        # ).count(), 3, "TimeResourcesQueue should have 3 for chair after adding 3.")
        # self.assertEqual(TimeResourcesQueue.objects.filter(
        #     resource_item_code=self.timeResourceItem_cher1,
        #     segment=self.segment_task_wash,
        #     resource_model=self.resource_model_chair
        # ).count(), 3, "TimeResourcesQueue should have 3 for chair after adding 3.")
        # self.assertEqual(TimeResourcesQueue.objects.filter(
        #     resource_item_code=self.timeResourceItem_cher1,
        #     segment=self.segment_task_cut,
        #     resource_model=self.resource_model_chair
        # ).count(), 3, "TimeResourcesQueue should have 3 for chair after adding 3.")
        # self.assertEqual(TimeResourcesQueue.objects.filter(
        #     resource_item_code=self.timeResourceItem_cher1,
        #     segment=self.segment_task_color,
        #     resource_model=self.resource_model_chair
        # ).count(), 3, "TimeResourcesQueue should have 3 for chair after adding 3.")
        


         