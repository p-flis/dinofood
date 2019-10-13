from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404, JsonResponse
from django.conf import settings
<<<<<<< Updated upstream
from main_app.forms import RecipeForm
from main_app.models import *
=======
>>>>>>> Stashed changes
from accounts.models import *
from main_app.forms import *
from django.forms.formsets import formset_factory
from main_app.views import display_form_errors
from django.core.mail import send_mail
from django.urls import reverse
import django.views.generic as generic
import main_app.custom_mixins as custom_mixins
from django.urls import reverse_lazy
import django.contrib.auth.mixins as mixins


class RecipeList(generic.ListView):
    queryset = Recipe.objects.filter(accepted=True)
    context_object_name = "list_items"


class AddRecipe(mixins.LoginRequiredMixin, generic.CreateView):
    model = Recipe
    success_url = reverse_lazy('recipe')
    fields = [
        "name",
        'description',
        'recipe_text',
        'image',
        'tools'
    ]
    ingredient_form_set = None
    http_method_names = ['get', 'post']

    def dispatch(self, request, *args, **kwargs):
        self.ingredient_form_set = formset_factory(IngredientOptionForm, extra=2, min_num=1, validate_min=True)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        formset = self.ingredient_form_set()
        ingredients = Ingredient.objects.all().order_by('name')
        self.extra_context = {
            "ingredients": ingredients,
            'formset': formset
        }
        return super().get(request, *args, **kwargs)

    # todo: too long function. Make mixin for formset?
    def form_valid(self, form):
        formset = self.ingredient_form_set(self.request.POST, self.request.FILES)
        if not formset.is_valid():
            return super().form_invalid(form)

        i_list = []
        q_list = []
        u_list = []
        for f in formset:
            cd = f.cleaned_data
            i_list.append(Ingredient.objects.get(id=cd.get('ingredient')))
            q_list.append(cd.get('quantity'))
            u_list.append(Unit.objects.get(id=cd.get('unit')))

        response = super().form_valid(form)  # save model

        recipe_model = form.instance
        for i in range(len(i_list)):
            try:
                q = int(q_list[i])
                u = u_list[i]
                recipe_model.ingredients.add(i_list[i], through_defaults={'quantity': q, 'unit': u})
            except ValueError:
                print("what:")
                pass
        recipe_model.owner = self.request.user
        recipe_model.accepted = self.request.user.is_superuser
        recipe_model.save()

        # todo - move to models.py, auto after create
        if Recipe.objects.filter(accepted=False).count() == 1:
            send_mail(
                'Unaccepted recipes',
                'Sth happened.',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

        return response


class RecipeId(generic.DetailView):
    model = Recipe
    pk_url_kwarg = 'object_id'
    context_object_name = "item"

    def get_context_data(self, **kwargs):
        form = RecipeIdIngredientsForm(recipe=self.object)
        if self.request.user.is_authenticated:
            form.initial = {"ingredients": [ing.id for ing in self.request.user.ingredients.all()]}
            rating = Rating.objects.filter(recipe=self.object, user=self.request.user)
        else:
            rating = None
        self.extra_context = {
            "rating": rating,
            "form": form
        }
        return super().get_context_data(**kwargs)


class RecipeDelete(mixins.LoginRequiredMixin, generic.DeleteView):
    model = Recipe
    pk_url_kwarg = 'object_id'
    success_url = reverse_lazy('recipe')

    def delete(self, request, *args, **kwargs):
        if self.get_object().owner != request.user and not request.user.is_superuser:
            # I'm pretty sure this is not very secure
            return redirect('/accounts/login/?next=' + request.path)
        return super().delete(request, *args, **kwargs)


class AcceptRecipe(custom_mixins.SuperuserRequiredMixin, generic.ListView):
    queryset = Recipe.objects.filter(accepted=False)
    context_object_name = "list_items"


class RecipeIdRate(generic.detail.BaseDetailView):
    model = Recipe
    pk_url_kwarg = 'object_id'
    http_method_names = ['get', 'post']

    # todo: why too much data is bad?
    # todo: method like 'only' for dictionary?
    def render_to_response(self, context):
        context = {
            'rating': context['rating'],
            'mean': context['mean'],
            'favourite': context['favourite']
        }
        return JsonResponse(context)

    def get_context_data(self, **kwargs):
        mean = self.object.average_rating()
        if self.request.user.is_authenticated:
            user = self.request.user
            prev_rating = Rating.objects.filter(user=user, recipe=self.object)
            if len(prev_rating) > 0:
                self.extra_context = {'rating': prev_rating[0].rating, 'mean': mean,
                                      'favourite': prev_rating[0].favourite}
            else:
                self.extra_context = {'rating': None, 'mean': mean, 'favourite': False}
        else:
            self.extra_context = {'rating': None, 'mean': mean, 'favourite': False}
        return super().get_context_data(**kwargs)

    # todo: cleanup!!
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # messages.error(request, "") TODO:change to reporting an error for stardisplayer to understand
            return JsonResponse({'rating': None, 'mean': None, 'favourite': None})
        data = request.POST.copy()
        if data is None:
            return JsonResponse({'rating': None, 'mean': None, 'favourite': None})
        rating = data.get("rating")
        favourite = data.get("favourite")
        if favourite is None \
                or (favourite is False and rating is None) \
                or rating not in [None, '1', '2', '3', '4', '5']:
            return JsonResponse({'rating': None, 'mean': None, 'favourite': None})
        user = request.user
        recipe = self.get_object()
        prev_rating = Rating.objects.filter(user=user, recipe=recipe)
        if rating is None:  # the heart has been clicked, we edit only favourite
            if len(prev_rating) > 0:
                prev_rating = prev_rating[0]
                prev_rating.favourite = (data.get("favourite") == 'true')
                prev_rating.save()
                new_rating = prev_rating
            else:
                new_rating = Rating(user=user, recipe=recipe, rating=None, favourite=True)
        else:
<<<<<<< Updated upstream
            displayFormErrors(form)
        return redirect('/recipe')
    raise Http404


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def add_recipe_to_default(request):
    if request.method == 'GET':
        ingredients = Ingredient.objects.all()
        form = RecipeForm()
        return render(request, "food/new_recipe_form.html", {"ingredients": ingredients, 'form': form})
    elif request.method == 'POST':
        data = request.POST.copy()
        # needed only because of the ingredients not in form but in html
        form = RecipeForm(data=request.POST or None, files=request.FILES or None)
        if form.is_valid():
            recipe_model = form.save(commit=False)
            recipe_model.save()
            i_list = [Ingredient.objects.get(name=ing) for ing in data.getlist("ingredients")]
            q_list = data.getlist("quantities")
            for i in range(len(i_list)):
                try:
                    q = int(q_list[i])
                    recipe_model.ingredients.add(i_list[i], through_defaults={'quantity': q})
                except ValueError:
                    pass
            recipe_model.save()
            file_name = "default_db.json"
            with open(file_name, 'r', encoding='utf-8') as file:
                db = json.load(file)
                ingredients_data = []
                ingredient_names = data.getlist("ingredients")
                for i in range(len(i_list)):
                    ingredients_data.append({"name": ingredient_names[i],
                                             "quantity": int(q_list[i])})
                recipes_data = db['recipes']
                recipes_data.append({"name": form.cleaned_data["name"],
                                     "description": form.cleaned_data["description"],
                                     "recipe": form.cleaned_data['recipe'],
                                     "ingredients": ingredients_data})

            with open(file_name, 'w', encoding='utf-8') as file:
                json.dump(db, file)
        return redirect('/recipe')
    raise Http404


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def accept_recipes(request):
    recipes = Recipe.objects.filter(accepted=False)
    return render(request, "food/recipe.html", {"list_items": recipes})


def recipe_id(request, object_id):
    recipe_model = Recipe.objects.filter(id=object_id)
    if request.user.is_authenticated:
        rating = Rating.objects.filter(recipe=recipe_model[0], user=request.user)
    else:
        rating=None
    if not recipe_model:
        raise Http404
    return render(request, "food/recipe_id_get.html", {"item": recipe_model.get(id=object_id), "rating": rating})


@login_required(login_url='/accounts/login')
def recipe_id_delete(request, object_id):
    recipe_model = Recipe.objects.filter(id=object_id)
    if not recipe_model:
        raise Http404
    if recipe_model.get().owner != request.user and not request.user.is_superuser:
        # I'm pretty sure this is not very secure
        return redirect('/accounts/login/?next=' + request.path)
    recipe_model.delete()
    return redirect('/recipe')


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def recipe_id_accept(request, object_id):
    recipe_model = Recipe.objects.filter(id=object_id).update(accepted=True)
    if not recipe_model:
        raise Http404
    return redirect('/recipe/accept')
=======
            rating = int(rating)
            if len(prev_rating) > 0:
                prev_rating = prev_rating[0]
                if prev_rating.rating is None:
                    recipe.times_rated = recipe.times_rated + 1
                    recipe.sum_rating = recipe.sum_rating + rating
                else:
                    recipe.sum_rating = recipe.sum_rating - prev_rating.rating + rating
                prev_rating.rating = rating
                new_rating = prev_rating
            else:
                new_rating = Rating(user=user, recipe=recipe, rating=rating, favourite=False)
                recipe.sum_rating = recipe.sum_rating + rating
                recipe.times_rated = recipe.times_rated + 1

        new_rating.save()
        recipe.save()
        mean = recipe.average_rating()
        output_data = {'rating': new_rating.rating, 'mean': mean, 'favourite': new_rating.favourite}
        return JsonResponse(output_data)


class RecipeIdAccept(custom_mixins.SuperuserRequiredMixin, generic.detail.SingleObjectMixin, generic.RedirectView):
    model = Recipe
    pk_url_kwarg = 'object_id'
    url = reverse_lazy('accept_recipes')

    def get(self, request, *args, **kwargs):
        recipe_model = self.get_object()
        recipe_model.accepted = True
        recipe_model.save()
        return super().get(request, *args, **kwargs)
>>>>>>> Stashed changes
