from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from decimal import Decimal

from dmessages.views import new_conversation, inbox
from dmessages.forms import NewConversationForm, MessageForm
from dmessages.models import Conversation, Message

class NewConversationTestCase(TestCase):
    def setUp(self):
        self.password = 'password'
        self.user1 = User.objects.create_user(
            username='user1',
            password=self.password
            )
        self.user2 = User.objects.create_user(
            username='user2',
            password=self.password
            )
        self.url = reverse('new_conversation')
        self.response = self.client.get(self.url)

class NewConversationRequiresLogin(NewConversationTestCase):
    def test_new_conversation_requires_log_in(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))
class NewConversationFormLoggedInTests(NewConversationTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username='user1', password=self.password)
        self.response = self.client.get(self.url)
    # Basic stuff
    def test_new_conversation_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    def test_new_conversation_url_resolves_new_conversation_view(self):
        view = resolve('/messages/new_conversation')
        self.assertEquals(view.func, new_conversation)
    def test_new_conversation_contains_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
    def test_new_conversation_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, NewConversationForm)

class NewConversationSuccesfulNewConversation(NewConversationTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username='user1', password=self.password)
        self.response = self.client.post(self.url, {
            'name': 'Test Conversation 1',
            'send_to': self.user2.id,
            'message': 'Test message lol',
            'reason': 'Buy'
        })
    def test_new_conversation_new_conversation_created(self):
        self.assertEquals(Conversation.objects.count(), 1)

class InboxViewTestCase(TestCase):
    def setUp(self):
        self.password = 'password'
        self.user1 = User.objects.create_user(
            username='user1',
            password=self.password
            )
        self.user2 = User.objects.create_user(
            username='user2',
            password=self.password
            )
        self.conversation = Conversation.objects.create(
            name = 'Test Conversation',
            created_by = self.user1,
            send_to = self.user2,
            reason = 'Buy'
        )
        self.url = reverse('inbox', kwargs={'pk':self.user1.id})
class InboxLoginRequired(InboxViewTestCase):
    def InboxRequiresLogIn(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))
class InboxLoggedInTests(InboxViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username='user1', password=self.password)
        self.response = self.client.get(self.url)
    # Basic stuff
    def test_inbox_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    def test_inbox_url_resolves_inbox_view(self):
        view = resolve('/messages/inbox/{pk}'.format(pk=self.conversation.id))
        self.assertEquals(view.func, inbox)
    def test_inbox_contains_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
    def test_inbox_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, MessageForm)
class InboxSuccesfulMessageSent(InboxViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username='user1', password=self.password)
        self.response = self.client.post(self.url, {
            'message' : 'Test message'
        })
    def test_inbox_sucessful_message_creation(self):
        self.assertEquals(Message.objects.count(), 1)
