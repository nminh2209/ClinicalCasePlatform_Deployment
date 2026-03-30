import sys

# Import Celery app only in Celery processes to avoid heavy task-module imports
# when booting the web service workers.
if any("celery" in arg.lower() for arg in sys.argv):
	from .celery import app as celery_app

	__all__ = ("celery_app",)
else:
	__all__ = ()
