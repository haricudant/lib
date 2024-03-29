from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from django.urls import reverse #Used to generate urls by reversing the URL patterns


# from django.contrib.auth.models import User

# # Create user and save to the database
# user = User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')
#
# # Update fields and then save again
# user.first_name = 'John'
# user.last_name = 'Citizen'
# user.save()
class Genre(models.Model):
    """
    Model representing a book genre (e.g. Science Fiction, Non Fiction).
    """
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")
    
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name
        
        
# class Language(models.Model):
#     """
#     Model representing a Language (e.g. English, French, Japanese, etc.)
#     """
#     name = models.CharField(max_length=200, help_text="Enter a the book's natural language (e.g. English, French, Japanese etc.)")
#
#     def __str__(self):
#         """
#         String for representing the Model object (in Admin site etc.)
#         """
#         return self.name
        
        
class Book(models.Model):
    """
    Model representing a book (but not a specific copy of a book).
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
      # Foreign Key used because book can only have one author, but authors can have multiple books
      # Author as a string rather than object because it hasn't been declared yet in file.
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN',max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
      # ManyToManyField used because Subject can contain many books. Books can cover many subjects.
      # Subject declared as an object because it has already been defined.
    # language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
      
    def display_genre(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
        display_genre.short_description = 'Genre'
    
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title
        
        
import uuid # Required for unique book instances
from datetime import date

from django.contrib.auth.models import User #Required to assign User as a borrower

class BookInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True) 
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
        

    LOAN_STATUS = (
        ('d', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status= models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='d', help_text='Book availability')

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)   

    def __str__(self):
        """
        String for representing the Model object.
        """
        #return '%s (%s)' % (self.id,self.book.title)
        return '{0} ({1})'.format(self.id,self.book.title)
        

class Author(models.Model):
    """
    Model representing an author.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ["last_name","first_name"]
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('author-detail', args=[str(self.id)])
    

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '{0}, {1}'.format(self.last_name,self.first_name)


class Subcription_type_quarterly(models.Model):
    quarterly = models.CharField(max_length=200)

    def __str__(self):
        return  self.quarterly
class Subscription_type_monthly(models.Model):
    monthly = models.CharField(max_length=200)

    def __str__(self):
        return self.monthly

class Subscription_type_halfyearly(models.Model):
    halfyearly = models.CharField(max_length=200)

class Subscription_type_annual(models.Model):
    annual = models.CharField(max_length=200)

        #
        #
        # null=True, max_length=100,
        # default=None,
        # choices=SMART_PHONE_OWNERSHIP, verbose_name='Do you own a Smartphone?')


#
# #If 'Yes' How many hours a day do you access the Internet on it?
#     Monthly_Subscription = 'Monthly 15 Euros'
#     Quarterly_Subscription = '25 Euros For three months'
#     HalfYearly_Subscription = '45 Euros for Half a Year'
#     Annual_subscription = '75 Euros per Year'
#
#
#     SMART_PHONE_USAGE = (
#         (Monthly_Subscription , '15 Euros'),
#         (Quarterly_Subscription, '25 Euros'),
#         (HalfYearly_Subscription, '45 Euros'),
#         (Annual_subscription, '75 Euros')
#
#                )
#
#     smart_phone_usage = models.CharField(
#         null=True, blank=True, max_length=100,
#         choices=SMART_PHONE_USAGE,
#         # default=None,
#         verbose_name='What type of subscription you need?'
#         )
