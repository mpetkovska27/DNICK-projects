from django.db import models

# Create your models here.

class Movie(models.Model):
    GENRE_CHOICES = [
        ('Horror', 'Horror'),
        ('Romance', 'Romance'),
        ('Sci-Fi', 'Sci-Fi'),
        ('Fantasy', 'Fantasy'),
        ('Action', 'Action'),
    ]
    title = models.CharField(max_length=50, blank=True, null=True )
    description = models.TextField(blank=True, null=True )
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    average_rating = models.FloatField(blank=True, null=True )

    def __str__(self):
        return self.title

    def update_rating(self):
        reviews = Review.objects.filter(movie=self)
        if reviews.exists():
            self.average_rating = sum(r.rating for r in reviews)/reviews.count()
        else:
            self.average_rating = 0.0
        self.save()


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    rating = models.IntegerField(choices=[(1, str(i)) for i in range(1,6)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.movie.update_rating()