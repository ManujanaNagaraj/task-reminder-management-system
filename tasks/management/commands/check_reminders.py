from django.core.management.base import BaseCommand
from django.utils import timezone
from tasks.models import Task

class Command(BaseCommand):
    help = 'Checks for tasks with due reminders and prints a notification'

    def handle(self, *args, **options):
        now = timezone.now()
        # Filter for incomplete tasks where reminder_time is in the past or now
        due_tasks = Task.objects.filter(is_completed=False, reminder_time__lte=now)

        if not due_tasks.exists():
            self.stdout.write(self.style.SUCCESS('No due reminders found.'))
            return

        for task in due_tasks:
            message = f"Reminder: Task '{task.title}' for user {task.user.username} is due!"
            self.stdout.write(self.style.WARNING(message))
