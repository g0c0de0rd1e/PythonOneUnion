from django import forms
from django.contrib.auth import get_user_model
from .models import ChatMessage

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['recipient', 'content']
        labels = {
            'recipient': 'Recipient',
            'content': 'Message'
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5})
        }

    def clean_recipient(self):
        recipient = self.cleaned_data['recipient']
        if not recipient.is_active or recipient.username == 'anonymous':
            raise forms.ValidationError("Invalid recipient")
        return recipient
