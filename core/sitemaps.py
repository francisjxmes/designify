from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from portfolio.models import PortfolioItem


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return ["home", "portfolio_list", "order_list"]

    def location(self, item):
        return reverse(item)


class PortfolioSitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return PortfolioItem.objects.all()

    def location(self, item):
        return reverse("portfolio_detail", args=[item.pk])