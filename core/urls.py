from django.urls import path, include

from django.contrib import admin

from django.conf.urls.static import static
from django.conf import settings

import main_app.views
import main_app.dish_views.ingredient_views as ingredient_views
import main_app.dish_views.recipe_views as recipe_views
import main_app.dish_views.search_views as search_views
import main_app.tests.test_views as test_views

admin.autodiscover()

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", main_app.views.index, name="index"),
    # path("db/", base.views.db, name="db"),
    path("admin/", admin.site.urls),

    path('accounts/', include('accounts.urls')),  # first search in accounts app
    path('accounts/', include('django.contrib.auth.urls')),  # then in built in auth

    path("recipe/", recipe_views.recipe, name="recipe"),
    path("recipe/new", recipe_views.add_recipe, name="add_recipe"),
    path("test/recipe/new", recipe_views.add_recipe_to_default, name="add_recipe_to_default"),
    path("recipe/accept", recipe_views.accept_recipes, name="accept_recipes"),
    path("recipe/<int:dish_id>", recipe_views.recipe_id, name="recipe_id"),
    path("recipe/<int:dish_id>/delete", recipe_views.recipe_id_delete, name="recipe_delete"),
    path("recipe/<int:dish_id>/accept", recipe_views.recipe_id_accept, name="recipe_accept"),

    path("recipe/search", search_views.recipe_search, name="search_recipe"),

    path("ingredient/", ingredient_views.ingredient, name="ingredient"),
    path("ingredient/new", ingredient_views.add_ingredient, name="add_ingredient"),
    path("test/ingredient/new", ingredient_views.add_ingredient_to_default, name="add_ingredient_to_default"),
    path("ingredient/<int:ing_id>", ingredient_views.ingredient_id, name="ingredient_id"),
    path("ingredient/<int:ing_id>/delete", ingredient_views.ingredient_id_delete, name="ingredient_delete"),
    path("ingredient/<int:ing_id>/update", ingredient_views.ingredient_id_update, name="ingredient_update"),

    path("test/empty", main_app.tests.test_views.test_empty_database, name="test_empty_database"),
    path("test/default", main_app.tests.test_views.test_default_database, name="test_default_database"),
    # path("test/default_big", main_app.tests.test_views.test_big_database, name="test_big_database"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)