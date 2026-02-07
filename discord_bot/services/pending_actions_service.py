from asgiref.sync import sync_to_async
from discord_bot.models import PendingAction


@sync_to_async
def get_pending_actions() :
    return list(PendingAction.objects.filter(done=False))

@sync_to_async
def mark_action_done(action) :
    action.done = True
    action.save()