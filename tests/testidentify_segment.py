from django.test import TestCase
from config.models import Segment, OrderItems, ModalCount, SegmentParam, Orders

class SegmentRetrievalTest(TestCase):
    def setUp(self):
        # Create a SegmentParam instance first
        self.segment_param = SegmentParam.objects.create(
            code='TASK',
            name='Test Param',
            description='Test Description',
            container=False,
            contained=False,
            available=False,
            working=False,
            active=False,
            paid=False,
            calc_pay=0,
            calc_available=0
        )

        # Then create a Segment instance, passing the SegmentParam instance
        self.segment = Segment.objects.create(
            code='BOB',
            type='Test Type',
            segment_param=self.segment_param
        )

        # Now, create the ModalCount instance, passing the Segment instance
        self.modal_count = ModalCount.objects.create(
            code=self.segment, 
            name='Test Modal Count', 
            description='Description for Test Modal Count', 
            duration=30, 
            price=100.00, 
            max_quantity=1, 
            logic='AND', 
            sub=0
        )

        self.order = Orders.objects.create(
            order_number='123456',
            item_count=1,
            order_price=100.00,
        )
        
        self.order_item = OrderItems.objects.create(
            order = self.order,
            modal_count=self.modal_count,
            item_name='Test Item',
            unit_price=100.00,
            order_number=self.order.order_number,
        )

    def test_segment_retrieval(self):
        assert Segment.objects.count() == 1, "Segment instance was not created."
        assert SegmentParam.objects.count() == 1, "SegmentParam instance was not created."
        assert self.modal_count.code == self.segment, "ModalCount is not linked to the correct Segment."
        assert self.order_item.modal_count == self.modal_count, "OrderItem's ModalCount is not linked correctly."


        # Attempt to retrieve the segment based on the order item's modal count
        segment = Segment.objects.filter(code=self.order_item.modal_count.code.code).first()
        assert segment is not None, "Failed to retrieve the Segment based on OrderItem's ModalCount."
                
        # Check that the segment was successfully retrieved
        self.assertIsNotNone(segment, "Segment was not retrieved successfully")
        self.assertEqual(segment.code, self.modal_count.code.code, "Retrieved segment does not match expected modal count code")
