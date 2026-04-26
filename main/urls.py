from django.urls import path

from main import views

app_name = 'main'

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('addgame/', views.ProductAddView.as_view(), name='add_game'),
    path('catalog/', views.ProductListView.as_view(), name='catalog'),
    path('updategame/<slug:update_slug>', views.UpdateProductView.as_view(), name='update_game'),
    path('deletegame/<slug:delete_slug>', views.ProductDeleteView.as_view(), name='delete_game'),
    path('catalog/<slug:category_slug>', views.ProductListView.as_view(), name='product_by_category'),
    path('<slug:product_slug>', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/', views.CategoryListView.as_view(), name='category'),


]