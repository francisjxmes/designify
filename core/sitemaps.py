from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from portfolio.models import PortfolioItem

class StaticViewSitemap(Sitemap):
    priority = 0.8

    def items(self):
        return ["home", "portfolio_list", "order_list"]

    def location(self, item):
        return reverse(item)

class PortfolioSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return PortfolioItem.objects.all()
