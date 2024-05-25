from django.contrib import admin

from apps.tgbot.models import User, SubscribeChat, FAQ, Mailing

from .tasks import add


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ['created']
    search_fields = ['user_id']


@admin.register(SubscribeChat)
class SubscribeChatAdmin(admin.ModelAdmin):
    search_fields = ['name', 'url']
    list_filter = ['created', 'updated']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    search_fields = ['title', 'description', 'message']
    list_filter = ['created', 'updated']


@admin.register(Mailing)
class MailingsAdmin(admin.ModelAdmin):
    actions = ['process_mailing']

    def process_mailing(self, request, queryset):
        for mailing in queryset:
            for user in mailing.users.all():
                add.delay(user.user_id, mailing.message)

    process_mailing.short_description = 'Начать рассылку'
