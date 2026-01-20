#!/usr/bin/env python3
"""Fix attachment handling in case creation"""
import re

file_path = r'd:\Download\randoms\HN2.1ProjectA-develop\HN2.1ProjectA-develop\backend\cases\views.py'

# Read file
with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# Find all perform_create methods and update them
i = 0
replacements_made = 0

while i < len(lines):
    # Look for perform_create method
    if 'def perform_create(self, serializer):' in lines[i] and 'Auto-assign repository' in lines[i+1]:
        print(f"Found perform_create at line {i+1}")
        
        # Find the end of the method (next def or class)
        j = i + 1
        while j < len(lines) and not (lines[j].strip().startswith('def ') and lines[j][0:4] == '    '):
            j += 1
        
        # Check if we need to modify this method
        method_lines = lines[i:j]
        method_text = ''.join(method_lines)
        
        if 'MedicalAttachment' not in method_text:
            print(f"  Needs update (no MedicalAttachment handling)")
            
            # Find the imports section
            import_idx = None
            for k in range(len(method_lines)):
                if 'from repositories.models import Repository' in method_lines[k]:
                    import_idx = k
                    break
            
            if import_idx is not None:
                # Add MedicalAttachment import
                method_lines[import_idx] = method_lines[import_idx].rstrip() + '\n        from .medical_models import MedicalAttachment\n'
            
            # Find serializer.save calls and replace them
            for k in range(len(method_lines)):
                if '            serializer.save(repository=repository)' in method_lines[k]:
                    method_lines[k] = method_lines[k].replace(
                        'serializer.save(repository=repository)',
                        'case = serializer.save(repository=repository)'
                    )
                elif '            serializer.save()' in method_lines[k]:
                    method_lines[k] = method_lines[k].replace(
                        'serializer.save()',
                        'case = serializer.save()'
                    )
            
            # Add attachment handling code before the method ends
            attachment_code = """
        # Process attachments from multipart upload
        request_data = self.request.data
        attachment_keys = [key for key in request_data.keys() if key.startswith('attachment_')]
        
        for key in attachment_keys:
            file = request_data[key]
            # Create MedicalAttachment
            MedicalAttachment.objects.create(
                case=case,
                file=file,
                attachment_type='other',  # Default type
                title=file.name,
                uploaded_by=self.request.user,
                file_size=file.size,
                file_type=file.content_type or '',
            )

"""
            method_lines.insert(-1, attachment_code)
            
            # Replace in original lines
            lines[i:j] = method_lines
            replacements_made += 1
            
            # Adjust i to skip the modified section
            i = i + len(method_lines)
        else:
            print(f"  Already has MedicalAttachment handling")
            i += 1
    else:
        i += 1

print(f"\nTotal replacements made: {replacements_made}")

if replacements_made > 0:
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("File updated successfully!")
else:
    print("No changes needed.")
