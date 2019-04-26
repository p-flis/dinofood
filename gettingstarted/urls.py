from django.urls import path, include

from django.contrib import admin
from django.views.generic import RedirectView

admin.autodiscover()

import hello.views
import hello.test_views
import hello.dish_views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", hello.views.index, name="index"),
    # path("db/", hello.views.db, name="db"),
    path("admin/", admin.site.urls),

    # najpierw szuka sb w aplikacji accounts
    path('accounts/', include('accounts.urls')),
    # a dopiero potem we wbudowanym auth
    path('accounts/', include('django.contrib.auth.urls')),

    path("recipe/", hello.dish_views.recipe, name="recipe"),
    path("recipe/new", hello.dish_views.add_recipe, name="add_recipe"),
    path("recipe/<int:dish_id>", hello.dish_views.recipe_id, name="recipe_id"),
    path("", hello.views.index, name="search_recipe"),
    path("ingredient/", hello.dish_views.ingredient, name="ingredient"),
    path("ingredient/new", hello.dish_views.add_ingredient, name="add_ingredient"),
    path("ingredient/<int:ing_id>", hello.dish_views.ingredient_id, name="ingredient_id"),
    path("category/", hello.dish_views.category, name="category"),
    path("category/new", hello.dish_views.add_category, name="add_category"),
    path("category/<int:cat_id>", hello.dish_views.category_id, name="category_id"),
    path("test/empty", hello.test_views.test_empty_database, name="test_empty_database"),
    path("test/default", hello.test_views.test_default_database, name="test_default_database"),
]
