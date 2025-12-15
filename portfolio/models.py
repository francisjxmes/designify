from django.db import models

class PortfolioItem(models.Model):
    title = models.CharField(max_length=120)
    category = models.CharField(max_length=60)  # e.g. Logo, Poster, Icon
    description = models.TextField()
    image = models.ImageField(upload_to="portfolio/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    client_name = models.CharField(max_length=80)
    quote = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.client_name} ({self.rating}/5)"

