"""
Fix script to add attachment handling to both CaseListCreateView classes
"""

def fix_perform_create():
    """
    This script updates the perform_create method in both CaseListCreateView classes
    to handle file attachments during case creation.
    
    Manual steps:
    1. Find line ~266 (first CaseListCreateView perform_create)
    2. Find line ~2334 (second CaseListCreateView perform_create)
    3. In BOTH methods, change:
       - serializer.save(repository=repository) → case = serializer.save(repository=repository)
       - serializer.save() → case = serializer.save()
    4. Add after the repository handling logic and before the next method:
    
        # Process attachments from multipart upload
        from .medical_models import MedicalAttachment
        request_data = self.request.data
        attachment_keys = [key for key in request_data.keys() if key.startswith('attachment_')]
        
        for key in attachment_keys:
            file = request_data[key]
            # Create MedicalAttachment
            MedicalAttachment.objects.create(
                case=case,
                file=file,
                attachment_type='other',  # Default type, can be enhanced
                title=file.name,
                uploaded_by=self.request.user,
                file_size=file.size,
                file_type=file.content_type or '',
            )
    """
    pass

if __name__ == "__main__":
    print(__doc__)
    print(fix_perform_create.__doc__)
