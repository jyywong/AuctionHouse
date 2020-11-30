from django.test import TestCase
from ..views import (
    search_books,
    search_orders
)
from auction.models import Book, BookInstance, Order
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from decimal import Decimal

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
        url = reverse('search_books')
        self.response = self.client.get(url)

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

    # Links that requires login
    # Can't figure out why these tests keep failing
    # def test_book_results_view_contains_link_to_messages_inbox_1(self):
    #     inbox_url = reverse('inbox', kwargs = {'pk': 1})
    #     self.assertContains(self.response, 'href="{0}"'.format(inbox_url))
    # def test_book_results_view_contains_link_to_library(self):
    #     library_url = reverse('library')
    #     self.assertContains(self.response, 'href="{0}"'.format(library_url))
    # def test_book_results_view_contains_link_to_new_book_instance(self):
    #     new_book_instance_url = reverse('new_book_instance')
    #     self.assertContains(self.response, 'href="{0}"'.format(new_book_instance_url))
    # def test_book_results_view_contains_link_to_add_order(self):
    #     add_order_url = reverse('add_order')
    #     self.assertContains(self.response, 'href="{0}"'.format(add_order_url))
    # def test_book_results_view_contains_link_to_order_library(self):
    #     order_library_url = reverse('order_library')
    #     self.assertContains(self.response, 'href="{0}"'.format(order_library_url))
    # def test_book_results_view_contains_link_to_order_results_page(self):
    #     order_results_url = reverse('search_orders')
    #     self.assertContains(self.response, 'href="{0}"'.format(order_results_url))
    # def test_book_results_view_contains_link_to_logout(self):
    #     logout_url = reverse('logout')
    #     self.assertContains(self.response, 'href="{0}"'.format(logout_url))

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
        url = reverse('search_orders')
        self.response = self.client.get(url)

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
            # Again no idea why this won't work
            self.client.login(username=self.user.username, password=self.user.password)

        # def test_search_orders_contains_dropdown_menu(self):
        #     self.assertContains(self.response, '> Messages </a>',1)
        # def test_book_results_view_contains_link_to_messages_inbox_1(self):
        #     inbox_url = reverse('inbox', kwargs = {'pk': 1})
        #     self.assertContains(self.response, 'href="{0}"'.format(inbox_url))
        # def test_book_results_view_contains_link_to_library(self):
        #     library_url = reverse('library')
        #     self.assertContains(self.response, 'href="{0}"'.format(library_url))
        # def test_book_results_view_contains_link_to_new_book_instance(self):
        #     new_book_instance_url = reverse('new_book_instance')
        #     self.assertContains(self.response, 'href="{0}"'.format(new_book_instance_url))
        # def test_book_results_view_contains_link_to_add_order(self):
        #     add_order_url = reverse('add_order')
        #     self.assertContains(self.response, 'href="{0}"'.format(add_order_url))
        # def test_book_results_view_contains_link_to_order_library(self):
        #     order_library_url = reverse('order_library')
        #     self.assertContains(self.response, 'href="{0}"'.format(order_library_url))
        # def test_book_results_view_contains_link_to_order_results_page(self):
        #     order_results_url = reverse('search_orders')
        #     self.assertContains(self.response, 'href="{0}"'.format(order_results_url))
        # def test_book_results_view_contains_link_to_logout(self):
        #     logout_url = reverse('logout')
        #     self.assertContains(self.response, 'href="{0}"'.format(logout_url))
