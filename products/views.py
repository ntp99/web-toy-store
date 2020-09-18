from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.messages import info, warning, success
from urllib.parse import urlencode
from .models import Product, Review
from .forms import ProductFilterForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

def index_view(request):
    products = Product.objects.all()

    if 'reset' in request.GET:
        if 'sortfilt' in request.session:
            request.session.pop('sortfilt')
        return redirect(reverse('index'))

    settings = request.session.get('sortfilt', {})

    fromsettings = False
    sortorder = request.GET.get('sort', '')
    if len(sortorder) == 0:
        sortorder = settings.get('sort', 'name')
        fromsettings = True
    products = products.order_by(sortorder)
    settings['sort'] = sortorder

    search_form = ProductFilterForm(request.GET)
    # ignore form errors; just get any cleaned data available
    if search_form.is_valid():
        pass

    search_string = search_form.cleaned_data.get('product_search', None)
    if search_string:
        products = products.filter(name__icontains=search_string)
        settings['product_search'] = search_string
    elif 'product_search' in settings:
        val = settings.get('product_search')
        products = products.filter(name__icontains=val)
        fromsettings = True

    min_price = search_form.cleaned_data.get('min_price', None)
    if min_price:
        products = products.filter(price__gte=min_price)
        settings['min_price'] = float(min_price)
    elif 'min_price' in settings:
        val = settings.get('min_price')
        products = products.filter(price__gte=val)
        fromsettings = True

    max_price = search_form.cleaned_data.get('max_price', None)
    if max_price:
        products = products.filter(price__lte=max_price)
        settings['max_price'] = float(max_price)
    elif 'max_price' in settings:
        val = settings.get('max_price')
        products = products.filter(price__lte=val)
        fromsettings = True

    ave_rate = search_form.cleaned_data.get('ave_rate', None)
    if ave_rate:
        products = products.annotate(avgstars=Avg('review__stars')).filter(avgstars__gte=ave_rate)
        settings['ave_rate'] = float(ave_rate)
    elif 'ave_rate' in settings:
        val = settings.get('ave_rate')
        products = products.annotate(avgstars=Avg('review__stars')).filter(avgstars__gte=val)
        fromsettings = True
        
    request.session['sortfilt'] = settings
    if fromsettings:
        url = "{}?{}".format(reverse('index'), urlencode(settings))
        return redirect(url)

    return render(request, "products/index.html", {'products':products, 'search_form':ProductFilterForm(initial=search_form.cleaned_data)})


def details_view(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "products/details.html", {'product':product})

@login_required
def review_view(request, id):
    product = get_object_or_404(Product,id=id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            product.review_set.create(stars=form.cleaned_data['stars'], description = form.cleaned_data['description'], user=request.user)
            return redirect ('details', id=product.id)
    else:
            form = ReviewForm()
    return render(request, "products/review.html", {'form':form, 'product': product})
