from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404

from .models import *


def empty_database():
    Category.objects.all().delete()
    User.objects.all().delete()
    # two of above should be enough if relations were configured properly
    Ingredient.objects.all().delete()
    Dish.objects.all().delete()
    DishDetails.objects.all().delete()
    Rating.objects.all().delete()


def test_empty_database(request):
    empty_database()
    return render(request, "empty_database.html")


def test_default_database(request):
    empty_database()

    category_names = [
        "Przyprawy",
        "Miesa",
        "Warzywa",
        "Owoce",
        "Ryby",
        "Alkohol"
    ]
    Category.objects.bulk_create([Category(name=n) for n in category_names])

    ingredient_data = [
        ("Ketchup", 0, "Przyprawy"),
        ("Majonez", 0, "Przyprawy"),
        ("Pieprz", 0, "Przyprawy"),
        ("Sól", 0, "Przyprawy"),
        ("Gałka muszkatołowa", 0, "Przyprawy"),
        ("Zioła prowansalskie", 0, "Przyprawy"),

        ("Kurczak", 20, "Miesa"),
        ("Indyk", 30, "Miesa"),
        ("Świnia", 20, "Miesa"),
        ("Wół", 20, "Miesa"),
        ("Bóbr", 100, "Miesa"),
        ("Pies", 1, "Miesa"),

        ("Pomidor", 3, "Warzywa"),
        ("Marchewka", 1, "Warzywa"),
        ("Pietruszka", 2, "Warzywa"),
        ("Kartofle", 1, "Warzywa"),
    ]
    Ingredient.objects.bulk_create([Ingredient(name=n[0], price=n[1], category=Category.objects.get(name=n[2]))
                                    for n in ingredient_data])

    dish_data = [
        ("Kurczak z ketchupem",
            "Włóż kurczaka do ketchupa",
            ["Kurczak", "Ketchup"]),
        ("Zupa z bobra",
            "Bardzo dobra",
            ["Bóbr"]),
        ("Indyk po tunezyjsku",
            "Bardzo zagranicznie",
            ["Indyk", "Zioła prowansalskie", "Pomidor", "Marchewka", "Sól", "Pieprz"]),
        ("Obiad dla czworga",
            "Albo dla dóch głodnych",
            ["Kurczak", "Indyk", "Świnia", "Wół", "Pomidor", "Marchewka", "Kartofle", "Pieprz", "Sól"]),
        ("Żeberka",
            "Głównie z woła",
            ["Wół", "Ketchup", "Majonez", "Sól", "Pieprz", "Marchewka", "Kartofle", "Pies"]),
    ]
    for n in dish_data:
        d = Dish(name=n[0], description=n[1])
        d.save()
        for ing_name in n[2]:
            d.ingredients.add(Ingredient.objects.get(name=ing_name), through_defaults={'quantity': 1})

    return render(request, "default_database.html")
