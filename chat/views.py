from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, View
from .models import ChatMessage, Chat, ChatParticipant
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseBadRequest

@method_decorator(login_required, name='dispatch')
class UserListView(ListView):
    model = User
    template_name = 'chat/chat_list.html'
    paginate_by = 20

    def get_queryset(self):
        return User.objects.all().exclude(id=self.request.user.id)

@method_decorator(login_required, name='dispatch')
class ChatView(View):
    def get(self, request, username):
        recipient = get_object_or_404(User, username=username)
        
        messages = ChatMessage.objects.filter(
            Q(sender=recipient, recipient=request.user) | 
            Q(sender=request.user, recipient=recipient)
        ).order_by('-timestamp')
        
        chats = Chat.objects.filter(
            Q(participants=request.user) & Q(participants=recipient)
        ).prefetch_related('last_message').select_related('last_message')
        
        context = {
            'messages': messages,
            'recipient': recipient,
            'chats': chats,
        }
        return render(request, 'chat/chat_with_user.html', context)

    def post(self, request, username):
        recipient = get_object_or_404(User, username=username)
        
        message_text = request.POST.get('message')
        if not message_text:
            return HttpResponseBadRequest("Сообщение не может быть пустым")
        
        ChatMessage.objects.create(
            sender=request.user,
            recipient=recipient,
            content=message_text
        )
        
        # Создаем или обновляем чат
        chat = Chat.objects.create()
        chat.participants.add(request.user, recipient)
        chat.last_message = ChatMessage.objects.filter(sender=request.user, recipient=recipient).order_by('-timestamp').first()
        chat.save()
        
        return redirect(f'/chat/chat-with-user/{username}/')

@login_required
def chat_with_user(request, username):
    recipient = get_object_or_404(User, username=username)
    
    if request.method == 'GET':
        # Обработка GET-запроса
        messages = ChatMessage.objects.filter(
            Q(recipient=recipient, sender=request.user) | 
            Q(sender=recipient, recipient=request.user)
        ).order_by('-timestamp')
        
        chats = Chat.objects.filter(Q(participants=request.user) & Q(participants=recipient)).prefetch_related('last_message').select_related('last_message')

        
        context = {
           'messages': messages,
           'recipient': recipient,
            'chats': chats,
        }
        return render(request, 'chat/chat_with_user.html', context)
    
    elif request.method == 'POST':
        # Обработка POST-запроса
        message_text = request.POST.get('message')
        if not message_text:
            return HttpResponseBadRequest("Сообщение не может быть пустым")
        
        ChatMessage.objects.create(
            sender=request.user,
            recipient=recipient,
            content=message_text
        )
        
        # Создаем или обновляем чат
        chat = Chat.objects.create()
        chat.participants.add(request.user, recipient)
        chat.last_message = ChatMessage.objects.filter(sender=request.user, recipient=recipient).order_by('-timestamp').first()
        chat.save()
        
        return JsonResponse({
           'message': message_text,
           'recipient_username': recipient.username
        })
    
    else:
        return HttpResponseBadRequest("Неподдерживаемый метод запроса")

@login_required
def join_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    participant = get_object_or_404(User, id=request.user.id)
    
    if not ChatParticipant.objects.filter(chat=chat, participant=participant).exists():
        ChatParticipant.objects.create(chat=chat, participant=participant)
        chat.last_message = ChatMessage.objects.filter(chat=chat).order_by('-timestamp').first()
        chat.save()
    
    return redirect(f'/chat/chat-with-user/{request.user.username}/')
