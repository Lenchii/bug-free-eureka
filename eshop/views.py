from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.views import View
from django.views.generic import TemplateView, FormView, CreateView, UpdateView
from eshop.models import Product, Cart, ProductReview, Category
from projekt_team.forms import ProductReviewForm
from django.views.generic.detail import DetailView
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

from django.http import JsonResponse


def api_search_view(request):
    query = request.GET.get("q")
    if query:
        res = {"products":
                   [(p.id, p.title)
                    for p in Product.objects.filter(title__icontains=query)]
               }
    else:
        res = {"products": []}

    return JsonResponse(res)

class ProductDetailView(DetailView):

    model = Product
    template_name = "product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = Category.objects.all()
        context["categories"]=categories

        if self.request.user.is_authenticated:
            user = self.request.user
            cart, created = Cart.objects.get_or_create(user=user)
            context['cart'] = cart

        categories = Category.objects.all()
        context["categories"] = categories

        return context

def hello_world_view(request):
    return HttpResponse ("Hello world")

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "Logout successful")
        return redirect("homepage")


class LoginView(FormView, TemplateView):
    template_name = "login.html"
    form_class = AuthenticationForm

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "Log in successfully")
            return redirect("homepage")

        messages.error(request, "Wrong credentials")
        return redirect("login")



# def homepage_view(request):
#    category = request.GET.get("category")
#
#   if category:
#       products = Product.objects.filter(category=category)
#   else:
#        products = Product.objects.all()
#
#    user = get_user_model().objects.first()
#    cart, created = Cart.objects.get_or_create(user=user)
#
#   context = {
#        "products": products,
#        "cart": cart
#    }
#    return TemplateResponse(request, "homepage.html", context=context)

class HomepageView (TemplateView):
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super (HomepageView, self).get_context_data (**kwargs)

        category = self.request.GET.get ("category")

        categories = Category.objects.all()

        if category:
            products = Product.objects.filter (category=category)
        else:
            products = Product.objects.all ()

        #user = get_user_model ().objects.first ()
        if self.request.user.is_authenticated:
            user=self.request.user
            cart, created = Cart.objects.get_or_create (user=user)
            context['cart']=cart

        context.update({
            "categories": categories,
            "products": products,

        })

        return context


def add_to_cart_view(request, item_pk):
    product = get_object_or_404 (Product, pk=item_pk)
    user = get_user_model ().objects.first ()
    cart, created = Cart.objects.get_or_create (user=user)
    cart.products.add (product)
    return redirect (request.META.get ('HTTP_REFERER', 'homepage'))


def remove_from_cart_view(request, item_pk):
    product = get_object_or_404 (Product, pk=item_pk)
    user = get_user_model ().objects.first ()
    cart, created = Cart.objects.get_or_create (user=user)
    cart.products.remove (product)
    return redirect (request.META.get ('HTTP_REFERER', 'homepage'))


def cart_view(request, pk):
    cart = get_object_or_404 (Cart, pk=pk)
    context = {
        "cart": cart
    }

    categories = Category.objects.all()
    context["categories"] = categories

    return TemplateResponse (request, "cart.html", context=context)


#class DeleteProductReview (View):
#
#   def get(self, request, pk, *args, **kwargs):
#      product_review = get_object_or_404 (ProductReview, pk=pk)
#     product_review.delete ()
#    return redirect (request.META.get ('HTTP_REFERER', 'homepage'))


class ListProductReviewView (FormView):
    template_name = "product_reviews.html"
    form_class = ProductReviewForm

    def get_initial(self):
        product = self.get_object ()
        user = get_user_model ().objects.first ()
        return {"product": product, "user": user}

    def get_object(self):
        return get_object_or_404 (Product, pk=self.kwargs["product_pk"])

    def get_context_data(self, **kwargs):
        context = super (ListProductReviewView, self).get_context_data (**kwargs)
        product = self.get_object ()
        user = get_user_model ().objects.first ()
        context.update ({
            "product": product,
            "cart": user.cart
        })

        categories = Category.objects.all()
        context["categories"] = categories

        return context

    def post(self, request, *args, **kwargs):
        product = get_object_or_404 (Product, pk=self.kwargs["product_pk"])
        user = get_user_model ().objects.first ()

        form_data = {
            "user": user.pk,
            "product": product.pk,
            "text": request.POST.get ("text"),
            "score": request.POST.get ("score")
        }
        bounded_form = ProductReviewForm (data=form_data)
        if not bounded_form.is_valid ():
            return JsonResponse (status=400, data={"message": "invalid_data"})

        ProductReview.objects.create (
            user=bounded_form.cleaned_data["user"],
            product=bounded_form.cleaned_data["product"],
            text=bounded_form.cleaned_data["text"],
            score=bounded_form.cleaned_data["score"],
        )

        return self.get (request, *args, **kwargs)

class DeleteProductReview(View):

    def get(self, request, pk, *args, **kwargs):
        review = get_object_or_404(ProductReview, pk=pk)
        review.delete()

        return redirect(request.META.get('HTTP_REFERER', 'homepage'))