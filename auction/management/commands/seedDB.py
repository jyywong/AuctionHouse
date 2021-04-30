from django.core.management.base import BaseCommand, CommandError
from auction.models import Book, Order
from django.contrib.auth.models import User
from factories.auctionFactories import * 

class Command(BaseCommand):
    help = 'Seeds the database with factories'

    def handle(self, *args, **options):
        for i in range(10):
            try:
                self.stdout.write(UserFactory())
            except:
                raise CommandError('Something went wrong with the user factory')
        
        for i in range(10):
            try:
                BookFactory()
            except:
                raise CommandError('Something went wrong with the book factory')
        
        for i in range(500):
            try:
                OrderFactory()
            except: 
                raise CommandError('Something went wrong with the order factory')

        self.stdout.write(self.style.SUCCESS('Succesfully seeded database.'))