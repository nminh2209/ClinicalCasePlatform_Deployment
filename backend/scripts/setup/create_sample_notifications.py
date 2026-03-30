#!/usr/bin/env python
"""
Create sample notifications for testing
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clinical_case_platform.settings")
django.setup()

from notifications.models import Notification
from accounts.models import User
from cases.models import Case


def create_sample_notifications():
    print("🔔 Creating Sample Notifications")
    print("=" * 50)

    try:
        # Get a student user
        student = User.objects.filter(role="student").first()
        if not student:
            print("❌ No student user found. Please run populate_test_data.py first.")
            return

        # Get an instructor
        instructor = User.objects.filter(role="instructor").first()
        if not instructor:
            print("❌ No instructor found. Please run populate_test_data.py first.")
            return

        # Get some cases
        cases = Case.objects.all()[:3]
        if not cases:
            print("❌ No cases found. Please create some cases first.")
            return

        print(f"✅ Found student: {student.email}")
        print(f"✅ Found instructor: {instructor.email}")
        print(f"✅ Found {len(cases)} cases")
        print()

        # Create notifications for student
        notifications_data = [
            {
                "recipient": student,
                "notification_type": "grade",
                "title": "Bệnh án đã được chấm điểm",
                "message": f"Bài nộp của bạn cho '{cases[0].title}' đã được chấm điểm: 92%",
                "related_case": cases[0],
                "action_url": f"/cases/{cases[0].id}",  # type: ignore[attr-defined]
            },
            {
                "recipient": student,
                "notification_type": "comment",
                "title": "Nhận xét mới",
                "message": f"{instructor.get_full_name()} đã nhận xét về chẩn đoán phân biệt của bạn",
                "related_case": cases[0],
                "action_url": f"/cases/{cases[0].id}#comments",  # type: ignore[attr-defined]
            },
            {
                "recipient": student,
                "notification_type": "feedback",
                "title": "Phản hồi mới",
                "message": f"Bạn đã nhận được phản hồi mới cho bệnh án '{cases[1].title}'",
                "related_case": cases[1],
                "action_url": f"/cases/{cases[1].id}#feedback",  # type: ignore[attr-defined]
            },
            {
                "recipient": student,
                "notification_type": "reminder",
                "title": "Nhắc nhở hạn nộp",
                "message": f"Bệnh án '{cases[2].title}' sẽ hết hạn trong 2 ngày",
                "related_case": cases[2],
                "action_url": f"/cases/{cases[2].id}",  # type: ignore[attr-defined]
            },
        ]

        # Create instructor notifications
        instructor_notifications = [
            {
                "recipient": instructor,
                "notification_type": "submission",
                "title": "Sinh viên nộp bài",
                "message": f"{student.get_full_name()} đã nộp bệnh án '{cases[0].title}'",
                "related_case": cases[0],
                "action_url": f"/cases/{cases[0].id}",  # type: ignore[attr-defined]
            },
            {
                "recipient": instructor,
                "notification_type": "comment",
                "title": "Nhận xét mới từ sinh viên",
                "message": f"{student.get_full_name()} đã nhận xét về bệnh án '{cases[1].title}'",
                "related_case": cases[1],
                "action_url": f"/cases/{cases[1].id}#comments",  # type: ignore[attr-defined]
            },
        ]

        # Create the notifications
        created_count = 0
        for notif_data in notifications_data + instructor_notifications:
            notification = Notification.objects.create(**notif_data)
            print(
                f"✅ Created: {notification.title} for {notification.recipient.email}"
            )
            created_count += 1

        print()
        print(f"🎉 Successfully created {created_count} sample notifications!")
        print(f"   - {len(notifications_data)} for student ({student.email})")
        print(
            f"   - {len(instructor_notifications)} for instructor ({instructor.email})"
        )

    except Exception as e:
        print(f"❌ Error creating sample notifications: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    create_sample_notifications()
