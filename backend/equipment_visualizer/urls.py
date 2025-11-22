"""
equipment_visualizer URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    """Basic health check"""
    return JsonResponse({'status': 'ok', 'message': 'Backend is running'})

def db_check(request):
    """Database connection and table check"""
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        
        # Check if tables exist
        from equipment_api.models import Dataset
        dataset_count = Dataset.objects.count()
        
        return JsonResponse({
            'status': 'ok',
            'database': 'connected',
            'tables': 'exist',
            'dataset_count': dataset_count
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'database': 'error',
            'error': str(e),
            'type': type(e).__name__
        }, status=500)

urlpatterns = [
    path('', health_check),
    path('health/', health_check),
    path('db-check/', db_check),
    path('admin/', admin.site.urls),
    path('api/', include('equipment_api.urls')),
]
