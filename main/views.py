from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from cart.forms import CartProductAddForm
from .forms import AddProductsForm
from .models import Product, Category, Color, Size


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()[:8]
        context['categories'] = Category.objects.all()
        return context




class ProductListView(ListView):
    model = Product
    template_name = 'main/product_list.html'
    context_object_name = 'products'
    paginate_by = 1

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        sort = self.request.GET.get('sort', '')
        queryset = Product.objects.filter(available=True)
        self.category = None


        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=self.category)

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(category__name__icontains=query)
            )

        if sort and sort != 'all':
            if sort == 'newest':
                queryset = queryset.order_by('-created_at')
            elif sort == 'top-rated':
                queryset = queryset.order_by('-rating')
            elif sort == 'featured':
                queryset = queryset.filter(badges__slug='featured')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['category'] = self.category
        context['selected_sort'] = self.request.GET.get('sort', 'none')
        context['search_query'] = self.request.GET.get('q', '')

        return context

    def get_template_names(self):
        if self.request.headers.get('HX-Request') == 'true':
            hx_target = self.request.headers.get('HX-Target')

            if hx_target == 'catalog-shell':
                return ['main/partials/category_results.html']

            if hx_target == 'product-results':
                return ['main/partials/product_results.html']

        return ['main/product_list.html']


class ProductDetailView(DetailView):
    model = Product
    template_name = 'main/product_detail.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sizes'] = Size.objects.all()
        context['cart_add_form'] = CartProductAddForm
        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'main/category.html'
    context_object_name = 'categories'


class ProductAddView(CreateView):
    model = Product
    form_class = AddProductsForm
    template_name = 'main/create_product.html'
    success_url = reverse_lazy('main:home')

    extra_context = {'title': 'Add Product', 'text': 'Fill in the product details below to add a new item to your store.'}

    def form_valid(self, form):
        print("FORM IS VALID")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("FORM ERRORS:", form.errors)
        return super().form_invalid(form)


class UpdateProductView(UpdateView):
    model = Product
    form_class = AddProductsForm
    template_name = 'main/create_product.html'
    success_url = reverse_lazy('main:catalog')
    slug_url_kwarg = 'update_slug'

    extra_context = {'title': 'Update Product', 'text': 'Fill in the product details below to change.'}

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'main/confirm_delete.html'
    success_url = reverse_lazy('main:catalog')
    slug_url_kwarg = 'delete_slug'
    context_object_name = 'product'

