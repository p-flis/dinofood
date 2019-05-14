from django.urls import path, include

from django.contrib import admin

import base.views
import base.dish_views.category_views as category_views
import base.dish_views.ingredient_views as ingredient_views
import base.dish_views.recipe_views as recipe_views
import base.dish_views.search_views as search_views
import base.tests.test_views as test_views

admin.autodiscover()

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

    path('accounts/', include('accounts.urls')),  # first search in accounts app
    path('accounts/', include('django.contrib.auth.urls')),  # then in built in auth

    path("recipe/", recipe_views.recipe, name="recipe"),
    path("recipe/new", recipe_views.add_recipe, name="add_recipe"),
    path("recipe/<int:dish_id>", recipe_views.recipe_id, name="recipe_id"),
    path("recipe/<int:dish_id>/delete", recipe_views.recipe_id_delete, name="recipe_delete"),

    path("ingredient/", ingredient_views.ingredient, name="ingredient"),
    path("ingredient/new", ingredient_views.add_ingredient, name="add_ingredient"),
    path("ingredient/<int:ing_id>", ingredient_views.ingredient_id, name="ingredient_id"),
    path("ingredient/<int:ing_id>/delete", ingredient_views.ingredient_id_delete, name="ingredient_delete"),
    path("ingredient/<int:ing_id>/update", ingredient_views.ingredient_id_update, name="ingredient_update"),

    path("category/", category_views.category, name="category"),
    path("category/new", category_views.add_category, name="add_category"),
    path("category/<int:cat_id>", category_views.category_id, name="category_id"),
    path("category/<int:cat_id>/delete", category_views.category_id_delete, name="category_delete"),
    path("category/<int:cat_id>/update", category_views.category_id_update, name="category_update"),

    path("recipe/search", search_views.recipe_search, name="search_recipe"),

    path("test/empty", base.tests.test_views.test_empty_database, name="test_empty_database"),
    path("test/default", base.tests.test_views.test_default_database, name="test_default_database"),
]
