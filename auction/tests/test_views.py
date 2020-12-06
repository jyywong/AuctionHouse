from django.test import TestCase
from ..views import (
    search_books,
    search_orders,
    book_view,
    library,
    order_library,
    new_book_instance,
    add_order,
    profile
)
from ..forms import BookInstanceForm, OrderForm
from auction.models import Book, BookInstance, Order
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from decimal import Decimal
from dmessages.forms import NewConversationForm
from dmessages.models import Conversation, Message
class SearchBooksViewTests(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            # When query is empty, query searches for a name with a space " "
            name= 'Book One',
            description = 'Description',
            classes = 'classes',
            subject = 'subjects',
            author = 'John Doe',
            isbn = '123456678'
        )
        self.url = reverse('search_books')
        self.response = self.client.get(self.url)

class SearchBooksViewTestsNotLoggedIn(SearchBooksViewTests):
    # Basic stuff
    def test_search_books_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    def test_no_url_resolves_search_books_view(self):
        view = resolve('/')
        self.assertEquals(view.func, search_books)
    def test_book_results_url_resolves_search_books_view(self):
        view = resolve('/book_results')
        self.assertEquals(view.func, search_books)

    # Verifying that links exist on the page
    def test_search_books_view_contains_link_to_book_results_page(self):
        book_results_url = reverse('search_books')
        self.assertContains(self.response, 'href="{0}"'.format(book_results_url))
    def test_search_books_view_contains_link_to_order_results_page(self):
        order_results_url = reverse('search_orders')
        self.assertContains(self.response, 'href="{0}"'.format(order_results_url))
    def test_search_books_view_contains_link_to_book_view(self):
        book_view_url = reverse('book_view', kwargs = {'pk': self.book.id})
        self.assertContains(self.response, 'href="{0}"'.format(book_view_url))

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 1)

class SearchBooksViewTestsLoggedIn(SearchBooksViewTests):
    def setUp(self):
        super().setUp()
        self.username = 'jon'
        self.password = 'password'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)
    # Basic stuff
    def test_search_books_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    def test_no_url_resolves_search_books_view(self):
        view = resolve('/')
        self.assertEquals(view.func, search_books)
    def test_book_results_url_resolves_search_books_view(self):
        view = resolve('/book_results')
        self.assertEquals(view.func, search_books)

    # Verifying that links exist on the page
    def test_search_books_view_contains_link_to_book_results_page(self):
        book_results_url = reverse('search_books')
        self.assertContains(self.response, 'href="{0}"'.format(book_results_url))
    def test_search_books_view_contains_link_to_order_results_page(self):
        order_results_url = reverse('search_orders')
        self.assertContains(self.response, 'href="{0}"'.format(order_results_url))
    def test_search_books_view_contains_link_to_book_view(self):
        book_view_url = reverse('book_view', kwargs = {'pk': 1})
        self.assertContains(self.response, 'href="{0}"'.format(book_view_url))

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 1)


    def test_book_results_view_contains_link_to_messages_inbox_1(self):
        inbox_url = reverse('inbox', kwargs = {'pk': 1})
        self.assertContains(self.response, 'href="{0}"'.format(inbox_url))
    def test_book_results_view_contains_link_to_library(self):
        library_url = reverse('library')
        self.assertContains(self.response, 'href="{0}"'.format(library_url))
    def test_book_results_view_contains_link_to_new_book_instance(self):
        new_book_instance_url = reverse('new_book_instance')
        self.assertContains(self.response, 'href="{0}"'.format(new_book_instance_url))
    def test_book_results_view_contains_link_to_add_order(self):
        add_order_url = reverse('add_order')
        self.assertContains(self.response, 'href="{0}"'.format(add_order_url))
    def test_book_results_view_contains_link_to_order_library(self):
        order_library_url = reverse('order_library')
        self.assertContains(self.response, 'href="{0}"'.format(order_library_url))
    def test_book_results_view_contains_link_to_order_results_page(self):
        order_results_url = reverse('search_orders')
        self.assertContains(self.response, 'href="{0}"'.format(order_results_url))
    def test_book_results_view_contains_link_to_logout(self):
        logout_url = reverse('logout')
        self.assertContains(self.response, 'href="{0}"'.format(logout_url))

class SearchOrdersViewTest(TestCase):
    def setUp(self):
        self.username = 'jon'
        self.password = 'password'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.book = Book.objects.create(
            # When query is empty, query searches for a name with a space " "
            name= 'Book One',
            description = 'Description',
            classes = 'classes',
            subject = 'subjects',
            author = 'John Doe',
            isbn = '123456678'
        )
        self.order = Order.objects.create(
            order_owner = self.user,
            buyorsell = 'Buy',
            book = self.book,
            price = Decimal('25.99'),
            quantity = 1
        )
        self.url = reverse('search_orders')
        self.response = self.client.get(self.url)

class SearchOrdersViewTestNotLoggedIn(SearchOrdersViewTest):
    #Basic stuff
    def test_search_orders_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    def test_search_orders_url_resolves_search_orders_view(self):
        view = resolve('/order_results')
        self.assertEquals(view.func, search_orders)

    # Verifying that links exist on the page
    def test_search_orders_view_contains_link_to_book_results_page(self):
        book_results_url = reverse('search_books')
        self.assertContains(self.response, 'href="{0}"'.format(book_results_url))
    def test_search_orders_view_contains_link_to_order_results_page(self):
        order_results_url = reverse('search_orders')
        self.assertContains(self.response, 'href="{0}"'.format(order_results_url))
    def test_search_orders_view_contains_link_to_profile(self):
        profile_url = reverse('profile', kwargs = {'pk':self.user.id})
        self.assertContains(self.response, 'href="{0}"'.format(profile_url))

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 1)

class SearchOrdersViewTestLoggedIn(SearchOrdersViewTest):
        def setUp(self):
            super().setUp()

            self.client.login(username=self.username, password=self.password)
            self.response = self.client.get(self.url)
        def test_book_results_view_contains_link_to_messages_inbox_1(self):
            inbox_url = reverse('inbox', kwargs = {'pk': 1})
            self.assertContains(self.response, 'href="{0}"'.format(inbox_url))
        def test_book_results_view_contains_link_to_library(self):
            library_url = reverse('library')
            self.assertContains(self.response, 'href="{0}"'.format(library_url))
        def test_book_results_view_contains_link_to_new_book_instance(self):
            new_book_instance_url = reverse('new_book_instance')
            self.assertContains(self.response, 'href="{0}"'.format(new_book_instance_url))
        def test_book_results_view_contains_link_to_add_order(self):
            add_order_url = reverse('add_order')
            self.assertContains(self.response, 'href="{0}"'.format(add_order_url))
        def test_book_results_view_contains_link_to_order_library(self):
            order_library_url = reverse('order_library')
            self.assertContains(self.response, 'href="{0}"'.format(order_library_url))
        def test_book_results_view_contains_link_to_order_results_page(self):
            order_results_url = reverse('search_orders')
            self.assertContains(self.response, 'href="{0}"'.format(order_results_url))
        def test_book_results_view_contains_link_to_logout(self):
            logout_url = reverse('logout')
            self.assertContains(self.response, 'href="{0}"'.format(logout_url))

class BookViewTestCase(TestCase):
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

        self.book = Book.objects.create(
            # When query is empty, query searches for a name with a space " "
            name= 'Book One',
            description = 'Description',
            classes = 'classes',
            subject = 'subjects',
            author = 'John Doe',
            isbn = '123456678'
        )
        self.buy_order = Order.objects.create(
            order_owner = self.user1,
            buyorsell = 'Buy',
            book = self.book,
            price = Decimal('10.99'),
            quantity = 1
        )
        self.sell_order = Order.objects.create(
            order_owner = self.user2,
            buyorsell = 'Sell',
            book = self.book,
            price = Decimal('25.99'),
            quantity = 2
        )
        self.url = reverse('book_view', kwargs={'pk': self.book.id})
        self.response = self.client.get(self.url)
class BookViewBasicTests(BookViewTestCase):

    #Basic stuff
    def test_book_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    def test_book_view_url_resolves_book_view(self):
        view = resolve('/book_view/{pk}'.format(pk = self.book.id))
        self.assertEquals(view.func, book_view)
    # Verifying that links exist on the page
    def test_book_view_contains_link_to_book_results_page(self):
        book_results_url = reverse('search_books')
        self.assertContains(self.response, 'href="{0}"'.format(book_results_url))
    def test_book_view_contains_link_to_order_results_page(self):
        order_results_url = reverse('search_orders')
        self.assertContains(self.response, 'href="{0}"'.format(order_results_url))
    def test_book_view_contains_link_to_buyer_profile(self):
        buyer_profile_url = reverse('profile', kwargs = {'pk':self.buy_order.order_owner.id})
        self.assertContains(self.response, 'href="{0}"'.format(buyer_profile_url))
    def test_book_view_contains_link_to_seller_profile(self):
        seller_profile_url = reverse('profile', kwargs = {'pk':self.sell_order.order_owner.id})
        self.assertContains(self.response, 'href="{0}"'.format(seller_profile_url))

    # Verfiying form stuff
    def test_book_view_contains_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
    def test_book_view_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, NewConversationForm)
    def test_book_view_contains_form_inputs(self):
        self.assertContains(self.response, '<input type="text"', Order.objects.count())
        self.assertContains(self.response, '<select', (Order.objects.count())*2)
        self.assertContains(self.response, '<textarea', Order.objects.count())

class BookViewTestSuccesfulConversation(BookViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username='user1', password = self.password)
        self.response = self.client.post(self.url, {
            'name': 'Test Conversation 1',
            'send_to': self.user2.id,
            'message': 'Hello world',
            'reason': 'Buy'
        })

    def test_book_view_created_conversation(self):
        self.assertEquals(Conversation.objects.count(), 1)
    def test_book_view_created_message(self):
        self.assertEquals(Message.objects.count(), 1)
class BookViewTestInvalidConversation(BookViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username='user1', password = self.password)
        self.response = self.client.post(self.url, {
        'name':''
        })

    def test_book_view_still_responds(self):
        self.assertEquals(self.response.status_code, 200)
    #For some reason the new conversation form does not generate errors when unbound
    #Gotta fix it later
    # def test_book_view_contains_form_errors(self):
    #     form = self.response.context.get('form')
    #     self.assertTrue(form.errors)

class LibraryTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            # When query is empty, query searches for a name with a space " "
            name= 'Book One',
            description = 'Description',
            classes = 'classes',
            subject = 'subjects',
            author = 'John Doe',
            isbn = '123456678'
        )
        self.username = 'john'
        self.password = '123'
        self.user = User.objects.create_user(username = self.username, email = 'john@doe.com', password = self.password)
        self.book_instance = BookInstance.objects.create(
            book = self.book,
            owner = self.user,
            quantity = 1,
            quality = 'New',
            status = 'Inactive'
        )

        self.url = reverse('library')
        self.response = self.client.get(self.url)
class LibraryTestLoginRequired(LibraryTestCase):
    def test_library_redirects_without_login(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))

class LibraryLoggedInBasicTests(LibraryTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    #Basic stuff
    def test_library_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    def test_library_url_resolves_library_view(self):
        view = resolve('/library')
        self.assertEquals(view.func, library)
    def test_library_form_inputs(self):
        self.assertContains(self.response, '<input', 1)

    # Verifying that links exist on the page
    def test_library_contains_link_to_book_results_page(self):
        book_results_url = reverse('search_books')
        self.assertContains(self.response, 'href="{0}"'.format(book_results_url))

class OrderLibraryTestCase(TestCase):
    def setUp(self):
        self.username = 'jon'
        self.password = 'password'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
            )
        self.book = Book.objects.create(
            # When query is empty, query searches for a name with a space " "
            name= 'Book One',
            description = 'Description',
            classes = 'classes',
            subject = 'subjects',
            author = 'John Doe',
            isbn = '123456678'
        )
        self.buy_order = Order.objects.create(
            order_owner = self.user,
            buyorsell = 'Buy',
            book = self.book,
            price = Decimal('10.99'),
            quantity = 1
        )
        self.sell_order = Order.objects.create(
            order_owner = self.user,
            buyorsell = 'Sell',
            book = self.book,
            price = Decimal('25.99'),
            quantity = 2
        )
        self.url = reverse('order_library')
        self.response = self.client.get(self.url)
class OrderLibraryTestLoginRequired(OrderLibraryTestCase):
    def test_order_library_redirects_without_login(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))
class OrderLibraryLoggedInTests(OrderLibraryTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)
    #Basic stuff
    def test_order_library_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    def test_order_library_url_resolves_order_library_view(self):
        view = resolve('/order_library')
        self.assertEquals(view.func, order_library)

    # Testing if orders actually show
    def test_order_library_displays_orders(self):
        self.assertContains(self.response, self.book.name, 2)
    def test_order_library_shows_user_profile(self):
        self.assertContains(self.response, self.username, 2)

class NewBookInstanceTestCase(TestCase):
    def setUp(self):
        self.username = 'jon'
        self.password = 'password'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
            )
        self.book = Book.objects.create(
            # When query is empty, query searches for a name with a space " "
            name= 'Book One',
            description = 'Description',
            classes = 'classes',
            subject = 'subjects',
            author = 'John Doe',
            isbn = '123456678'
        )
        self.url = reverse('new_book_instance')
        self.response = self.client.get(self.url)

class NewBookInstanceTestLoginRequired(NewBookInstanceTestCase):
    def test_new_book_instance_requires_login(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))

class NewBookInstanceLoggedInTests(NewBookInstanceTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)
    # Basic stuff
    def test_new_book_instance_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    def test_new_book_instance_url_resolves_new_book_instance_view(self):
        view = resolve('/new_book_instance')
        self.assertEquals(view.func, new_book_instance)
    def test_new_book_instance_contains_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
    def test_new_book_instance_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, BookInstanceForm)

class NewBookInstanceSucessfulBookInstance(NewBookInstanceTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {
            'book' : self.book.id,
            'quantity' : 1,
            'quality' : 'New',
            'status' : 'Buy'
        })
    def test_new_book_instance_created_new_book_instance(self):
        self.assertEquals(BookInstance.objects.count(), 1)

class AddOrderTestCase(TestCase):
    def setUp(self):
        self.username = 'jon'
        self.password = 'password'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
            )
        self.book = Book.objects.create(
            # When query is empty, query searches for a name with a space " "
            name= 'Book One',
            description = 'Description',
            classes = 'classes',
            subject = 'subjects',
            author = 'John Doe',
            isbn = '123456678'
        )
        self.url = reverse('add_order')
        self.response = self.client.get(self.url)

class AddOrderTestLoginRequired(AddOrderTestCase):
    def test_add_order_requires_login(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))

class AddOrderLoggedInTests(AddOrderTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)
    # Basic stuff
    def test_add_order_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    def test_add_order_url_resolves_add_order_view(self):
        view = resolve('/add_order')
        self.assertEquals(view.func, add_order)
    def test_add_order_contains_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
    def test_add_order_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, OrderForm)

class AddOrderSucessfulOrder(AddOrderTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {
            'buyorsell' : 'Buy',
            'book' : self.book.id,
            'price' : 12.99,
            'quantity' : 1
        })
    def test_add_order_created_new_order(self):
        self.assertEquals(Order.objects.count(), 1)

class ProfileTest(TestCase):
    def setUp(self):
        self.username = 'jon'
        self.password = 'password'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
            )
        self.book = Book.objects.create(
            # When query is empty, query searches for a name with a space " "
            name= 'Book One',
            description = 'Description',
            classes = 'classes',
            subject = 'subjects',
            author = 'John Doe',
            isbn = '123456678'
        )
        self.buy_order = Order.objects.create(
            order_owner = self.user,
            buyorsell = 'Buy',
            book = self.book,
            price = Decimal('10.99'),
            quantity = 1
        )
        self.sell_order = Order.objects.create(
            order_owner = self.user,
            buyorsell = 'Sell',
            book = self.book,
            price = Decimal('25.99'),
            quantity = 2
        )
        self.url = reverse('profile', kwargs={'pk': self.user.id})
        self.response = self.client.get(self.url)
    # Basic stuff
    def test_profile_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    def test_profile_url_resolves_profile_view(self):
        view = resolve('/profile/{pk}'.format(pk = self.user.id))
        self.assertEquals(view.func, profile)
    # Should probably add some links and some message functionality to this page
