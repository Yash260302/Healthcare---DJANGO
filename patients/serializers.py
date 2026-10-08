from rest_framework import serializers

from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"
        read_only_fields = ("created_by", "created_at", "updated_at")

    def validate_age(self, value):
        if value > 150:
            raise serializers.ValidationError("Enter a valid age.")
        return value