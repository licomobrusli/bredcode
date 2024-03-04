from django.test import TestCase
from config.models import ModalCount, Orders, OrderItems, Phase, Segment, SegmentParam
from config.submit_order import identify_phases_for_order_item

class IdentifyPhasesForOrderItemTests(TestCase):
    def setUp(self):
        # Set up Segment params needed by segment
        self.segment_param = SegmentParam.objects.create(
            code='SP01',
            name='Segment Param 1',
            description='A test segment param',
            container=False,
            contained=True,
            available=False,
            working=True,
            active=True,
            paid=True,
            calc_pay=0,
            calc_available=-1
        )
        
        # Set up Segment needed by ModalCount
        self.segment = Segment.objects.create(
            code='SG01',  # Or whatever fields are required for Segment
            type='MC',
            segment_param=self.segment_param
        )

        # Set up ModalCount with a Segment instance instead of a string for 'code'
        self.modal_count = ModalCount.objects.create(
            code=self.segment,  # Pass the Segment instance here
            name='Test Modal Count',
            description='Description for Test Modal Count',
            duration=10,
            price=100.00,
            max_quantity=10,
            logic='NOT',
            sub=0,
            sequence=1,
        )

        # set up Order
        self.order = Orders.objects.create(
            order_number='123456',
            item_count=1,
            order_price=100,
        )

        # Set up OrderItem
        self.order_item = OrderItems.objects.create(
            modal_count=self.modal_count,
            item_name='Test Item',
            unit_price=100,
            item_count=1,
            item_price=100,
            order=self.order,
        )

        # Set up Phases in sequence
        self.phase1 = Phase.objects.create(
            code='PH01',
            name='Phase 1',
            modal_count=self.modal_count,
            sequence=1,
            duration=10
        )
        self.phase2 = Phase.objects.create(
            code='PH02',
            name='Phase 2',
            modal_count=self.modal_count,
            sequence=2,
            duration=15
        )


    def test_identify_phases_for_order_item(self):
        # Test that the phases are identified correctly for the order item
        identified_phases = identify_phases_for_order_item(self.order_item)
        expected_phases = [self.phase1, self.phase2]

        self.assertEqual(list(identified_phases), expected_phases, "The identified phases should match the expected phases in order")

        # Additional checks can be added here, such as checking the order of phases
        for i, phase in enumerate(identified_phases):
            self.assertEqual(phase.sequence, i + 1, f"The phase sequence should be {i + 1}")

