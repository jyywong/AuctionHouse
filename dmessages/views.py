from django.shortcuts import render, redirect
from .models import Conversation, Message
from .forms import *
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.


@login_required
def new_conversation(request):
    template = 'new_conversation2.html'
    queryset = Conversation.objects.filter(
        Q(created_by=request.user) |
        Q(send_to=request.user)
    ).order_by('-modified_at')
    form = NewConversationForm()

    context = {
        'conversations': queryset,
        'form': form
    }

    if request.method == 'POST':
        form = NewConversationForm(request.POST)
        if form.is_valid():
            conversation = form.save(commit=False)
            conversation.created_by = request.user
            conversation.save()
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                receiver=form.cleaned_data.get('send_to'),
                message=form.cleaned_data.get('message')
            )
            return redirect('inbox', pk=1)
    else:
        form = NewConversationForm()
    return render(request, template, context)


# def inbox(request):
#     # Deals with the messages and tabs
#     queryset = Conversation.objects.order_by('-modified_at')
#     template = 'inbox2.html'
#
#     first_convo = queryset.first()
#     second_convo = queryset[1]
#     third_convo = queryset[2]
#     fourth_convo = queryset[3]
#
#     messages = Message.objects.all()
#     user = request.user
#
#     # Deals with entering a new message
#
#
#     context = {
#         'conversations': queryset,
#         'first_convo':first_convo,
#         'second_convo':second_convo,
#         'third_convo':third_convo,
#         'fourth_convo':fourth_convo,
#         'messages':messages,
#         'user':user
#         }
#
#     return render(request, template, context)

'''
Realized that I don't know how to give the conversation ID back to the view if
I use the bootstrap javascript listgroup implementation. I need the conversation
ID to save the message to the appropriate conversation. I will have to hardcode
the conversation ID via url pk in the tabs :/

In the future: Learn JS and figure out how to give the conversation ID back to
view without hardcoding.
'''


@login_required
def inbox(request, pk):

    queryset = Conversation.objects.filter(
        Q(created_by=request.user) |
        Q(send_to=request.user)
    ).order_by('-modified_at')
    template = 'inbox3.html'
    messages = Message.objects.all()
    convo_messages = Message.objects.filter(conversation = pk).order_by('created_at')
    last_message = convo_messages.last()
    user = request.user
    form = MessageForm()
    context = {
        'conversations': queryset,
        'messages': messages,
        'pk': pk,
        'user': user,
        'form': form,
        'last_message': last_message
    }

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form_object = form.save(commit=False)
            form_object.conversation = Conversation.objects.get(id=pk)
            form_object.sender = request.user
            form_object.receiver = Conversation.objects.get(id=pk).send_to
            form_object.reason = 'Other'
            form_object.save()
            return render(request, template, context)
    else:
        form = MessageForm()
    return render(request, template, context)
