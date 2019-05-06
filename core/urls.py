from django.urls import path, include

from django.contrib import admin
from django.views.generic import RedirectView

admin.autodiscover()

import base.views
import base.test_views
import base.dish_views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", base.views.index, name="index"),
    # path("db/", base.views.db, name="db"),
    path("admin/", admin.site.urls),

    # najpierw szuka sb w aplikacji accounts
    path('accounts/', include('accounts.urls')),
    # a dopiero potem we wbudowanym auth
    path('accounts/', include('django.contrib.auth.urls')),

    path("recipe/", base.dish_views.recipe, name="recipe"),
    path("recipe/new", base.dish_views.add_recipe, name="add_recipe"),
    path("recipe/search", base.dish_views.recipe_search, name="search_recipe"),
    path("recipe/<int:dish_id>", base.dish_views.recipe_id, name="recipe_id"),
    path("recipe/<int:dish_id>/delete", base.dish_views.recipe_id_delete, name="recipe_delete"),
    path("ingredient/", base.dish_views.ingredient, name="ingredient"),
    path("ingredient/new", base.dish_views.add_ingredient, name="add_ingredient"),
    path("ingredient/<int:ing_id>", base.dish_views.ingredient_id, name="ingredient_id"),
    path("ingredient/<int:ing_id>/delete", base.dish_views.ingredient_id_delete, name="ingredient_delete"),
    path("category/", base.dish_views.category, name="category"),
    path("category/new", base.dish_views.add_category, name="add_category"),
    path("category/<int:cat_id>", base.dish_views.category_id, name="category_id"),
    path("category/<int:cat_id>/delete", base.dish_views.category_id_delete, name="category_delete"),
    path("test/empty", base.test_views.test_empty_database, name="test_empty_database"),
    path("test/default", base.test_views.test_default_database, name="test_default_database"),
]
