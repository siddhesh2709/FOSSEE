from django.db import models
from django.contrib.auth.models import User
import json


class Dataset(models.Model):
    """Model to store uploaded datasets"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
        
        import pandas as pd
        df = pd.DataFrame(self.data)
        
        # Calculate statistics
        summary = {
            'total_count': len(df),
            'equipment_types': df['Type'].value_counts().to_dict(),
            'statistics': {
                'flowrate': {
                    'average': float(df['Flowrate'].mean()),
                    'min': float(df['Flowrate'].min()),
                    'max': float(df['Flowrate'].max()),
                    'std': float(df['Flowrate'].std())
                },
                'pressure': {
                    'average': float(df['Pressure'].mean()),
                    'min': float(df['Pressure'].min()),
                    'max': float(df['Pressure'].max()),
                    'std': float(df['Pressure'].std())
                },
                'temperature': {
                    'average': float(df['Temperature'].mean()),
                    'min': float(df['Temperature'].min()),
                    'max': float(df['Temperature'].max()),
                    'std': float(df['Temperature'].std())
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
