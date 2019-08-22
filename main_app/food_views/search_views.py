from django.shortcuts import render
from django.db.models import Count, Sum, F, FloatField, Case, When, Value
from main_app.forms import SearchForm
from django.http import Http404
from django.urls import reverse_lazy


from main_app.models import *
from accounts.models import *
from main_app.views import display_form_errors
import django.views.generic as generic
import main_app.custom_mixins as custom_mixins


# https://github.com/taranjeet/django-library-app/blob/master/djlibrary/templates/store/create_normal.html


class RecipeSearch(generic.FormView):
    form_class = SearchForm
    template_name = "main_app/recipe_search.html"
    success_url = "main_app/recipe_list.html"

    def get_initial(self):
        initial = {"extra_money": 999}
        if self.request.user.is_authenticated:
            initial.update({
                'ingredients_in_fridge': self.request.user.ingredients.all(),
                "tools_in_kitchen": self.request.user.tools.all()
            })
        return initial

    def form_valid(self, form):
        ingredients_in_fridge = form.cleaned_data["ingredients_in_fridge"]
        ingredients_in_recipe = form.cleaned_data["ingredients_in_recipe"]
        extra_money = int(form.cleaned_data["extra_money"])

        is_vegetarian = form.cleaned_data["is_vegetarian"]
        is_vegan = form.cleaned_data["is_vegan"]
        is_gluten_free = form.cleaned_data["is_gluten_free"]
        is_favourite = form.cleaned_data["is_favourite"]
        # print(form.cleaned_data)

        ingredients_in_recipe_len = len(ingredients_in_recipe)

        search_result = Recipe.objects

        search_result = search_result \
            .annotate(recipe_price=Sum(Case(
                When(recipeingredient__ingredient__in=ingredients_in_fridge, then=0),
                default=F('recipeingredient__quantity') * F('recipeingredient__ingredient__price') * F(
                    'recipeingredient__unit__amount'),
                output_field=FloatField()
            ))
            ).filter(recipe_price__gt=extra_money)

        # for s in search_result.all():
        #     print(s.recipe_price)
        # print(search_result.all())
        # print(search_result.query)

        ids_not_affordable = [item.id for item in search_result.all()]
        search_result = Recipe.objects.exclude(id__in=ids_not_affordable)

        if ingredients_in_recipe and any(ingredients_in_recipe):
            search_result = search_result \
                .filter(ingredients__in=ingredients_in_recipe) \
                .annotate(ing_num=Count('ingredients')) \
                .filter(ing_num=ingredients_in_recipe_len)

        if is_favourite and self.request.user.is_authenticated:
            user_favourites_ids = [rating.recipe.id for rating in
                                   Rating.objects.filter(favourite=True, user=self.request.user)]
            search_result = search_result.filter(id__in=user_favourites_ids)
        if is_vegetarian:
            search_result = search_result.filter(ingredients__is_vegetarian=True)
        if is_vegan:
            search_result = search_result.filter(ingredients__is_vegan=True)
        if is_gluten_free:
            search_result = search_result.filter(ingredients__is_gluten_free=True)

        return render(self.request, self.success_url, {"list_items": search_result.all()})
