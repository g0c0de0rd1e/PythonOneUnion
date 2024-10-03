from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatMessage(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chat_received_messages',
        verbose_name='Получатель',
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chat_sent_messages',
        verbose_name='Отправитель',
    )

    class Meta:
        verbose_name = 'Сообщение в чате'
        verbose_name_plural = 'Сообщения в чате'

    @property
    def is_read(self):
        return self.recipient == self.sender

    def __str__(self):
        return f"{self.sender} -> {self.recipient}: {self.content[:20]}"

    def mark_as_read(self):
        self.is_read = True
        self.save()

class Chat(models.Model):
    participants = models.ManyToManyField(User, through='ChatParticipant')
    last_message = models.OneToOneField(ChatMessage, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'

    def __str__(self):
        return f"Chat {self.id} between {', '.join([p.username for p in self.participants.all()])}"

class ChatParticipant(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat_participants')
    participant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_participated_in')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('chat', 'participant')

    def __str__(self):
        return f"{self.participant} in {self.chat}"
