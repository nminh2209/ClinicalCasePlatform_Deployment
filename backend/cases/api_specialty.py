# cases/api_specialty.py
"""
API endpoints for getting specialties and other dynamic choices
Frontend will fetch these instead of hardcoding values
"""

from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .specialty_models import Specialty, CasePriorityLevel, CaseComplexityLevel


class SpecialtySerializer(serializers.ModelSerializer):
    """Serializer for Specialty model"""
    
    class Meta:
        model = Specialty
        fields = ["id", "name", "english_name", "description"]


class PriorityLevelSerializer(serializers.ModelSerializer):
    """Serializer for Priority Level"""
    
    class Meta:
        model = CasePriorityLevel
        fields = ["id", "name", "key", "color"]


class ComplexityLevelSerializer(serializers.ModelSerializer):
    """Serializer for Complexity Level"""
    
    class Meta:
        model = CaseComplexityLevel
        fields = ["id", "name", "key", "description"]


class SpecialtyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for getting active specialties
    READ-ONLY: Users can view, but only admins can edit via Django admin
    """
    
    queryset = Specialty.objects.filter(is_active=True)
    serializer_class = SpecialtySerializer
    permission_classes = [AllowAny]  # Anyone can view specialties
    
    @action(detail=False, methods=["get"])
    def all_choices(self, request):
        """
        Get all active choices for case creation forms
        Returns specialties, priority levels, and complexity levels
        
        Example response:
        {
            "specialties": [{"id": 1, "name": "Tim mạch", ...}],
            "priorities": [{"id": 1, "name": "Thấp", "key": "low", ...}],
            "complexities": [{"id": 1, "name": "Dễ", "key": "easy", ...}]
        }
        """
        return Response({
            "specialties": SpecialtySerializer(
                Specialty.objects.filter(is_active=True),
                many=True
            ).data,
            "priorities": PriorityLevelSerializer(
                CasePriorityLevel.objects.filter(is_active=True),
                many=True
            ).data,
            "complexities": ComplexityLevelSerializer(
                CaseComplexityLevel.objects.filter(is_active=True),
                many=True
            ).data,
        })
