import json
from django.views import generic

import main_app.tests.functions as functions


<<<<<<< Updated upstream
def empty_database():
    Recipe.objects.all().delete()
    Ingredient.objects.all().delete()
    Unit.objects.all().delete()
    CookingTool.objects.all().delete()
    # User.objects.all().delete() #idk where it is and if it is safe to remove users
    RecipeIngredient.objects.all().delete()
    Rating.objects.all().delete()
=======
class TestEmptyDatabase(generic.TemplateView):
    template_name = "empty_database.html"

    def get(self, request, *args, **kwargs):
        functions.empty_database()
        return super().get(request, *args, **kwargs)
>>>>>>> Stashed changes


class TestDefaultDatabase(generic.TemplateView):
    template_name = "default_database.html"

    def get(self, request, *args, **kwargs):
        functions.empty_database()
        functions.load_db_from_json("default_db.json")
        return super().get(request, *args, **kwargs)


class SaveDatabaseToJson(generic.TemplateView):
    template_name = "default_database.html"

    def get(self, request, *args, **kwargs):
        db = functions.create_dictionary_from_db()
        file_name = "default_db.json"
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(db, file)
        return super().get(request, *args, **kwargs)
