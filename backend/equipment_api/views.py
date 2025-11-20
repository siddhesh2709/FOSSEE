from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.contrib.auth.models import User
import pandas as pd
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from datetime import datetime

from .models import Dataset, EquipmentRecord
from .serializers import DatasetSerializer, DatasetListSerializer, UserSerializer


@method_decorator(csrf_exempt, name='dispatch')
class DatasetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing equipment datasets
    """
    serializer_class = DatasetSerializer
    permission_classes = [AllowAny]  # Allow unauthenticated access for development
    
    def get_queryset(self):
        # Return all datasets for development (or filter by user if authenticated)
        if self.request.user.is_authenticated:
            return Dataset.objects.filter(user=self.request.user)
        return Dataset.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DatasetListSerializer
        return DatasetSerializer
    
    def create(self, request, *args, **kwargs):
        """Upload and parse CSV file"""
        if 'file' not in request.FILES:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        csv_file = request.FILES['file']
        
        # Validate file extension
        if not csv_file.name.endswith('.csv'):
            return Response(
                {'error': 'File must be a CSV'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Read CSV file
            df = pd.read_csv(csv_file)
            
            # Validate required columns
            required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return Response(
                    {'error': f'Missing required columns: {", ".join(missing_columns)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Convert to JSON format
            data = df.to_dict('records')
            
            # Create dataset (use authenticated user or create anonymous user)
            from django.contrib.auth.models import User
            user = request.user if request.user.is_authenticated else User.objects.get_or_create(username='anonymous')[0]
            
            dataset = Dataset.objects.create(
                user=user,
                filename=csv_file.name,
                data=data
            )
            
            # Create individual records (optional, for relational queries)
            for record in data:
                EquipmentRecord.objects.create(
                    dataset=dataset,
                    equipment_name=record['Equipment Name'],
                    equipment_type=record['Type'],
                    flowrate=float(record['Flowrate']),
                    pressure=float(record['Pressure']),
                    temperature=float(record['Temperature'])
                )
            
            # Cleanup old datasets (keep last 5)
            if user.username != 'anonymous':
                Dataset.cleanup_old_datasets(user, keep_count=5)
            
            serializer = self.get_serializer(dataset)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'Error processing CSV: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        """Get summary statistics for a dataset"""
        dataset = self.get_object()
        summary = dataset.get_summary()
        return Response(summary)
    
    @action(detail=True, methods=['get'])
    def pdf(self, request, pk=None):
        """Generate and download PDF report"""
        dataset = self.get_object()
        summary = dataset.get_summary()
        
        # Create PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#283593'),
            spaceAfter=12,
        )
        
        # Title
        elements.append(Paragraph("Chemical Equipment Analysis Report", title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Dataset info
        elements.append(Paragraph(f"<b>Dataset:</b> {dataset.filename}", styles['Normal']))
        elements.append(Paragraph(f"<b>Upload Date:</b> {dataset.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        elements.append(Paragraph(f"<b>Total Records:</b> {summary['total_count']}", styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Equipment Type Distribution
        elements.append(Paragraph("Equipment Type Distribution", heading_style))
        type_data = [['Equipment Type', 'Count']]
        for eq_type, count in summary['equipment_types'].items():
            type_data.append([eq_type, str(count)])
        
        type_table = Table(type_data, colWidths=[3*inch, 2*inch])
        type_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3f51b5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(type_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Statistics
        elements.append(Paragraph("Parameter Statistics", heading_style))
        stats_data = [['Parameter', 'Average', 'Min', 'Max', 'Std Dev']]
        
        for param in ['flowrate', 'pressure', 'temperature']:
            stats = summary['statistics'][param]
            stats_data.append([
                param.capitalize(),
                f"{stats['average']:.2f}",
                f"{stats['min']:.2f}",
                f"{stats['max']:.2f}",
                f"{stats['std']:.2f}"
            ])
        
        stats_table = Table(stats_data, colWidths=[1.5*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3f51b5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(stats_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Equipment Data
        elements.append(PageBreak())
        elements.append(Paragraph("Equipment Data", heading_style))
        
        data_rows = [['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temp']]
        for record in dataset.data[:20]:  # Limit to first 20 records
            data_rows.append([
                record['Equipment Name'],
                record['Type'],
                str(record['Flowrate']),
                str(record['Pressure']),
                str(record['Temperature'])
            ])
        
        if len(dataset.data) > 20:
            data_rows.append(['...', '...', '...', '...', '...'])
        
        data_table = Table(data_rows, colWidths=[1.8*inch, 1.3*inch, 1.1*inch, 1.1*inch, 1*inch])
        data_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3f51b5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(data_table)
        
        # Footer
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph(
            f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            styles['Normal']
        ))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        
        # Return PDF response
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="equipment_report_{dataset.id}.pdf"'
        return response


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """User login"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        serializer = UserSerializer(user)
        response = Response({
            'message': 'Login successful',
            'user': serializer.data
        })
        return response
    else:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    """User logout"""
    logout(request)
    return Response({'message': 'Logout successful'})


@api_view(['GET'])
@permission_classes([AllowAny])
def current_user(request):
    """Get current user info"""
    if request.user.is_authenticated:
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """User registration"""
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = User.objects.create_user(username=username, password=password, email=email)
    serializer = UserSerializer(user)
    
    return Response({
        'message': 'Registration successful',
        'user': serializer.data
    }, status=status.HTTP_201_CREATED)
