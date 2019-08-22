from django.shortcuts import redirect
from django.http import JsonResponse
from django.conf import settings
from accounts.models import *
from main_app.forms import *
from django.forms.formsets import formset_factory
from django.core.mail import send_mail
import django.views.generic as generic
import main_app.custom_mixins as custom_mixins
from django.urls import reverse_lazy
import django.contrib.auth.mixins as mixins


class RecipeUpdate(mixins.LoginRequiredMixin, generic.UpdateView):
    model = Recipe
    success_url = reverse_lazy('recipe')
    fields = [
        "name",
        'description',
        'recipe_text',
        'image',
        'tools'
    ]
    pk_url_kwarg = 'object_id'
    ingredient_form_set = None
    context_object_name = 'post'

    def dispatch(self, request, *args, **kwargs):
        self.ingredient_form_set = formset_factory(IngredientOptionForm, extra=0, min_num=1, validate_min=True)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        ings = RecipeIngredient.objects.filter(recipe=self.get_object())
        formset = self.ingredient_form_set(
            initial=[{'quantity': ing.quantity,
                      'unit': ing.unit.pk,
                      'ingredient': ing.ingredient.pk}
                     for ing in ings]
        )
        ingredients = Ingredient.objects.all().order_by('name')
        self.extra_context = {
            "ingredients": ingredients,
            'formset': formset
        }
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):

        #It is a copy of AddRecipe (temporary).

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

        for tmp in RecipeIngredient.objects.filter(recipe=self.get_object()):
            tmp.delete()

        for i in range(len(i_list)):
            try:
                q = int(q_list[i])
                u = u_list[i]
                self.get_object().ingredients.add(i_list[i], through_defaults={'quantity': q, 'unit': u})
            except ValueError:
                print("what:")
                pass

        post = form.save(commit=False)
        post.save()
        return redirect('/recipe/')

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
    object = None

    # todo: why too much data is bad?
    # todo: method like 'only' for dictionary?
    def render_to_response(self, context):
        context = {
            'rating': context.get('rating', None),
            'mean': context.get('mean', None),
            'favourite': context.get('favourite', None)
        }
        return JsonResponse(context)

    def get(self, request, *args, **kwargs):
        mean = self.object.average_rating()
        self.extra_context = {'mean': mean}
        if self.request.user.is_authenticated:
            user = self.request.user
            prev_rating = Rating.objects.filter(user=user, recipe=self.object)
            if len(prev_rating) > 0:
                self.extra_context['rating'] = prev_rating[0].rating
                self.extra_context['favourite'] = prev_rating[0].favourite
        return super().get(request, *args, **kwargs)

    # todo: cleanup!!
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # messages.error(request, "") TODO:change to reporting an error for stardisplayer to understand
            context = self.get_context_data()
            return self.render_to_response(context)
        data = request.POST.copy()
        if data is None:
            context = self.get_context_data()
            return self.render_to_response(context)
        rating = data.get("rating")
        favourite = data.get("favourite")
        if favourite is None \
                or (favourite is False and rating is None) \
                or rating not in [None, '1', '2', '3', '4', '5']:
            context = self.get_context_data()
            return self.render_to_response(context)
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
        self.extra_context = {'rating': new_rating.rating, 'mean': mean, 'favourite': new_rating.favourite}
        context = self.get_context_data()
        return self.render_to_response(context)


class RecipeIdAccept(custom_mixins.SuperuserRequiredMixin, generic.detail.SingleObjectMixin, generic.RedirectView):
    model = Recipe
    pk_url_kwarg = 'object_id'
    url = reverse_lazy('accept_recipes')

    def get(self, request, *args, **kwargs):
        recipe_model = self.get_object()
        recipe_model.accepted = True
        recipe_model.save()
        return super().get(request, *args, **kwargs)
