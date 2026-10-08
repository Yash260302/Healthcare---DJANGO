from rest_framework import serializers

from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"
        read_only_fields = ("created_by", "created_at", "updated_at")

    def validate_experience_years(self, value):
        if value > 70:
            raise serializers.ValidationError("Enter a valid number of years.")
        return value