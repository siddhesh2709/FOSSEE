from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Dataset, EquipmentRecord


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class EquipmentRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentRecord
        fields = ['id', 'equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature']


class DatasetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    records = EquipmentRecordSerializer(many=True, read_only=True)
    summary = serializers.SerializerMethodField()
    
    class Meta:
        model = Dataset
        fields = ['id', 'user', 'filename', 'uploaded_at', 'data', 'records', 'summary']
        read_only_fields = ['user', 'uploaded_at']
    
    def get_summary(self, obj):
        return obj.get_summary()


class DatasetListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing datasets"""
    user = UserSerializer(read_only=True)
    record_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Dataset
        fields = ['id', 'user', 'filename', 'uploaded_at', 'record_count']
    
    def get_record_count(self, obj):
        return len(obj.data) if obj.data else 0
