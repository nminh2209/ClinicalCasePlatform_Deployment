# cases/pdf_views.py
"""
PDF export views for cases
"""

from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Case
from .pdf_renderer import generate_case_pdf


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_case_pdf(request, pk):
    """
    Export a case as PDF
    
    GET /api/cases/{id}/export_pdf/
    
    Returns PDF file for download
    """
    case = get_object_or_404(Case, pk=pk)
    
    # Check permissions
    user = request.user
    if case.student != user and not user.is_instructor:
        return Response(
            {"error": "You don't have permission to export this case"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        pdf_buffer = generate_case_pdf(case)
        
        filename = f"case_{case.id}_{case.title[:30]}.pdf"
        filename = filename.replace(' ', '_')
        
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
    except Exception as e:
        return Response(
            {"error": f"Failed to generate PDF: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
