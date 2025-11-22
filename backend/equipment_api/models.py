from django.db import models
from django.contrib.auth.models import User
import json


class Dataset(models.Model):
    """Model to store uploaded datasets"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()  # Store parsed CSV data as JSON
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.filename} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"
    
    def get_summary(self):
        """Calculate summary statistics for the dataset"""
        if not self.data:
            return {}
        
        # Extract values
        flowrates = [float(row.get('Flowrate', 0)) for row in self.data if row.get('Flowrate')]
        pressures = [float(row.get('Pressure', 0)) for row in self.data if row.get('Pressure')]
        temperatures = [float(row.get('Temperature', 0)) for row in self.data if row.get('Temperature')]
        
        # Calculate std dev
        def std_dev(values):
            if not values:
                return 0
            mean = sum(values) / len(values)
            variance = sum((x - mean) ** 2 for x in values) / len(values)
            return variance ** 0.5
        
        # Equipment type counts
        type_counts = {}
        for row in self.data:
            eq_type = row.get('Type', 'Unknown')
            type_counts[eq_type] = type_counts.get(eq_type, 0) + 1
        
        # Calculate statistics
        summary = {
            'total_count': len(self.data),
            'equipment_types': type_counts,
            'statistics': {
                'flowrate': {
                    'average': sum(flowrates) / len(flowrates) if flowrates else 0,
                    'min': min(flowrates) if flowrates else 0,
                    'max': max(flowrates) if flowrates else 0,
                    'std': std_dev(flowrates)
                },
                'pressure': {
                    'average': sum(pressures) / len(pressures) if pressures else 0,
                    'min': min(pressures) if pressures else 0,
                    'max': max(pressures) if pressures else 0,
                    'std': std_dev(pressures)
                },
                'temperature': {
                    'average': sum(temperatures) / len(temperatures) if temperatures else 0,
                    'min': min(temperatures) if temperatures else 0,
                    'max': max(temperatures) if temperatures else 0,
                    'std': std_dev(temperatures)
                }
            }
        }
        
        return summary
    
    @classmethod
    def cleanup_old_datasets(cls, user, keep_count=5):
        """Keep only the last N datasets per user"""
        datasets = cls.objects.filter(user=user).order_by('-uploaded_at')
        if datasets.count() > keep_count:
            datasets_to_delete = datasets[keep_count:]
            for dataset in datasets_to_delete:
                dataset.delete()


class EquipmentRecord(models.Model):
    """Model to store individual equipment records"""
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='records')
    equipment_name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=100)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    
    def __str__(self):
        return f"{self.equipment_name} ({self.equipment_type})"
