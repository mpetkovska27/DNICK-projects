from django.db.models.signals import pre_delete, post_delete, pre_save
from django.dispatch import receiver
from .models import *

@receiver(pre_delete, sender=Author)
def reassign_books_before_author_delete(sender, instance, **kwargs):
    books_to_update = Book.objects.filter(author=instance).all()
    other_author = Author.objects.exclude(id=instance.id).first()
    if other_author:
        for book in books_to_update:
            book.author = other_author
            book.save()
            print(book.title)
        print(f"Books reassigned to {instance.name} to {other_author.name}")
    else:
        print(f"No other author available")

@receiver(post_delete, sender=Author)
def log_author_delete(sender, instance, **kwargs):
    AuthorLog.objects.create(
        name=instance.name,
        description=f"Author '{instance.name}' was deleted.",
    )
    print(f"Author deletion logged for {instance.name}")

@receiver(pre_save, sender=Book)
def set_book_size(sender, instance, **kwargs):
    if instance.pages is not None:
        if instance.pages < 100:
            instance.size = 'S'
        elif instance.pages < 300:
            instance.size = 'M'
        else:
            instance.size = 'L'