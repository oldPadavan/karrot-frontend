from django.core.management.base import BaseCommand

from foodsaving.conversations.models import Conversation, ConversationParticipant
from foodsaving.groups.models import Group


class Command(BaseCommand):
    """Ensure each model that should have a conversation has one."""

    def handle(self, *args, **options):
        def print(*args):
            self.stdout.write(' '.join([str(_) for _ in args]))

        def print_success(*args):
            self.stdout.write(self.style.SUCCESS(' '.join(str(_) for _ in args)))

        for group in Group.objects.all():

            # ensure we have a conversation

            if not group.conversation:
                group.conversation = Conversation.objects.create()
                group.save()

            # ensure the members are synced

            group.conversation.sync_users(group.members.all())

