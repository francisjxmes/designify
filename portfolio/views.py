from django.shortcuts import get_object_or_404, render
from .models import PortfolioItem, Testimonial

def portfolio_list(request):
    items = PortfolioItem.objects.all()
    testimonials = Testimonial.objects.all()[:6]
    return render(request, "portfolio/portfolio_list.html", {"items": items, "testimonials": testimonials})

def portfolio_detail(request, item_id):
    item = get_object_or_404(PortfolioItem, id=item_id)
    return render(request, "portfolio/portfolio_detail.html", {"item": item})
