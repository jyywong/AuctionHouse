from django import forms
from django.forms import ModelForm
from .models import *

class MessageForm(ModelForm):

    class Meta:
        model = Message
        fields = ['message']



class NewConversationForm(ModelForm):
    reason_choices=[
        ('Buy', 'I want to buy'),
        ('Sell', 'I want to sell'),
        ('Other', 'Other')
    ]
    message = forms.CharField(widget = forms.Textarea(), max_length=4000, required=True)
    class Meta:
        model = Conversation
        fields = ['name', 'send_to', 'message', 'reason']
        labels = {
            'name': 'Conversation Name'
        }
