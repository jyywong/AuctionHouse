from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.





class Conversation(models.Model):
    reason_choices=[
        ('Buy', 'Buy'),
        ('Sell', 'Sell'),
        ('Other', 'Other')
    ]
    name = models.CharField(max_length = 50)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    modified_at = models.DateTimeField(auto_now=True)
    send_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Conversation')
    reason = models.CharField(max_length=100, choices=reason_choices, default='Other')
    # Need a created by field
    def last_message (self):
        return Message.objects.filter(conversation=self).last()

class Message(models.Model):


    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='message')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'receiver')
    created_at = models.DateTimeField(auto_now_add=True)

    message = models.TextField()

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        new = self.pk is None
        super(Message, self).save(*args,**kwargs)
        if new:
            self.conversation.modified_at = timezone.now()
            self.conversation.save()
