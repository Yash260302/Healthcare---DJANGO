from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from patients.models import Patient

from .models import PatientDoctorMapping
from .serializers import MappingSerializer


class MappingListCreateView(generics.ListCreateAPIView):
    """POST /api/mappings/  and  GET /api/mappings/"""

    serializer_class = MappingSerializer

    def get_queryset(self):
        return (
            PatientDoctorMapping.objects.filter(patient__created_by=self.request.user)
            .select_related("patient", "doctor")
            .order_by("id")
        )


class MappingDetailView(APIView):
    """
    GET    /api/mappings/<patient_id>/  -> doctors assigned to that patient
    DELETE /api/mappings/<id>/          -> remove a mapping by its own id
    """

    def get(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk, created_by=request.user)
        mappings = (
            PatientDoctorMapping.objects.filter(patient=patient)
            .select_related("patient", "doctor")
            .order_by("id")
        )
        serializer = MappingSerializer(
            mappings, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def delete(self, request, pk):
        mapping = get_object_or_404(
            PatientDoctorMapping, pk=pk, patient__created_by=request.user
        )
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)