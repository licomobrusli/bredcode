from django.test import TestCase
from config.models import Phase, PhaseResource, ResourceType, ResourceModel, Segment, SegmentParam, ModalCount
from config.submit_order import identify_resources_for_phase  # Adjust import path as necessary

class IdentifyResourcesForPhaseTests(TestCase):
    def setUp(self):
        # Create necessary instances for ResourceType and ResourceModel
        self.time_resource_type = ResourceType.objects.create(
            code='T',
            name='Time Resource',
            measure='hours',
            unit_size=1
        )
        
        self.resource_model = ResourceModel.objects.create(
            code='RM01',
            name='Resource Model 1',
            type=self.time_resource_type,
            cost_per_unit=50.00,
            no_of_units=5,
            fungible=True
        )

        # Create necessary instances for Segment and SegmentParam if needed for Phase
        self.segment_param = SegmentParam.objects.create(
            code='SP01',
            name='Segment Param 1',
            description='A segment parameter',
            container=True,
            contained=False,
            available=True,
            working=True,
            active=True,
            paid=True,
            calc_pay=100,
            calc_available=1
        )
        
        self.segment = Segment.objects.create(
            code='SG01',
            type='Segment Type 1',
            segment_param=self.segment_param
        )
        
        # Assuming 'modal_count' in Phase is mandatory, create a ModalCount instance
        self.modal_count = ModalCount.objects.create(
            code=self.segment,
            name='Modal Name',
            description='Modal Description',
            duration=30,
            price=300.00,
            max_quantity=10,
            sequence=1
        )

        # Create Phase instance
        self.phase = Phase.objects.create(
            code='PH01',
            name='Phase 1',
            sequence=1,
            duration=60,
            modal_count=self.modal_count
        )

        # Create PhaseResource instance
        self.phase_resource = PhaseResource.objects.create(
            code='PR01',
            name='Phase Resource 1',
            phase_code=self.phase,
            resource_models_code=self.resource_model,
            resource_types_code=self.time_resource_type
        )

    def test_identify_resources_for_phase(self):
        # Call the function under test
        resources = identify_resources_for_phase(self.phase)

        # Check that the function returns the correct resources
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0], self.phase_resource)
        self.assertEqual(resources[0].resource_types_code, self.time_resource_type)
