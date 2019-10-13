from main_app.models import *


def int_from_decimal(number):
    return float(number)


def decimal_from_int(number):
    return number


class TestDatabase:
    @classmethod
    def append_custom_test_database(cls, *, units_data=None, ingredients_data=None, tools_data=None, recipes_data=None):
        if units_data:
            for unit_data in units_data:
                assert 'name' in unit_data
                unit_data.setdefault('amount', 1)
                Unit.objects.create(name=unit_data['name'], amount=decimal_from_int(unit_data['amount']))

        if ingredients_data:
            for ingredient_data in ingredients_data:
                assert 'name' in ingredient_data
                ingredient_data.setdefault('price', 1)
                ingredient_data.setdefault('is_vegetarian', False)
                ingredient_data.setdefault('is_vegan', False)
                ingredient_data.setdefault('is_gluten_free', False)
                ingredient_model = Ingredient(name=ingredient_data['name'],
                                              price=decimal_from_int(ingredient_data['price']),
                                              is_vegetarian=ingredient_data['is_vegetarian'],
                                              is_vegan=ingredient_data['is_vegan'],
                                              is_gluten_free=ingredient_data['is_gluten_free'])
                ingredient_model.save()
                if 'units' in ingredient_data and len(ingredient_data['units']) > 0:
                    for unit_data in ingredient_data['units']:
                        assert 'name' in unit_data
                        ingredient_model.units.add(Unit.objects.get(name=unit_data['name']))

        if tools_data:
            for tool_data in tools_data:
                assert 'name' in tool_data
                CookingTool.objects.create(name=tool_data['name'])

        if recipes_data:
            for recipe_data in recipes_data:
                assert 'name' in recipe_data
                recipe_data.setdefault('description', "")
                recipe_data.setdefault('recipe', "")
                if 'image' not in recipe_data or recipe_data['image'] == "":
                    recipe_data['image'] = "default.png"

                recipe_model = Recipe(name=recipe_data['name'],
                                      description=recipe_data['description'],
                                      recipe_text=recipe_data['recipe'],
                                      image=recipe_data['image'])
                recipe_model.save()
                for ingredient_data in recipe_data['ingredients']:
                    assert 'name' in ingredient_data
                    ingredient_data.setdefault('unit', "Gram")
                    ingredient_data.setdefault('quantity', 1)
                    ingredient_model = Ingredient.objects.get(name=ingredient_data['name'])
                    unit_model = ingredient_model.units.get(name=ingredient_data['unit'])
                    recipe_model.ingredients.add(ingredient_model,
                                                 through_defaults={'quantity': ingredient_data['quantity'],
                                                                   'unit': unit_model})
                if 'tools' in recipe_data:
                    for tool_data in recipe_data['tools']:
                        assert 'name' in tool_data
                        recipe_model.tools.add(CookingTool.objects.get(name=tool_data['name']))

    @classmethod
    def create_custom_test_database(cls, *, units_data=None, ingredients_data=None, tools_data=None, recipes_data=None):
        if units_data:
            for unit_data in units_data:
                assert 'name' in unit_data
                unit_data.setdefault('amount', 1)
                Unit.objects.create(name=unit_data['name'], amount=decimal_from_int(unit_data['amount']))

        if ingredients_data:
            for ingredient_data in ingredients_data:
                assert 'name' in ingredient_data
                ingredient_data.setdefault('price', 1)
                ingredient_data.setdefault('is_vegetarian', False)
                ingredient_data.setdefault('is_vegan', False)
                ingredient_data.setdefault('is_gluten_free', False)
                ingredient_model = Ingredient(name=ingredient_data['name'],
                                              price=decimal_from_int(ingredient_data['price']),
                                              is_vegetarian=ingredient_data['is_vegetarian'],
                                              is_vegan=ingredient_data['is_vegan'],
                                              is_gluten_free=ingredient_data['is_gluten_free'])
                ingredient_model.save()
                if 'units' in ingredient_data and len(ingredient_data['units']) > 0:
                    for unit_data in ingredient_data['units']:
                        assert 'name' in unit_data
                        if units_data and unit_data['name'] in [u['name'] for u in units_data]:
                            ingredient_model.units.add(Unit.objects.get(name=unit_data['name']))

        if tools_data:
            for tool_data in tools_data:
                assert 'name' in tool_data
                CookingTool.objects.create(name=tool_data['name'])

        if recipes_data:
            for recipe_data in recipes_data:
                assert 'name' in recipe_data
                recipe_data.setdefault('description', "")
                recipe_data.setdefault('recipe', "")
                if 'image' not in recipe_data or recipe_data['image'] == "":
                    recipe_data['image'] = "default.png"

                recipe_model = Recipe(name=recipe_data['name'],
                                      description=recipe_data['description'],
                                      recipe_text=recipe_data['recipe'],
                                      image=recipe_data['image'])
                recipe_model.save()
                for ingredient_data in recipe_data['ingredients']:
                    assert 'name' in ingredient_data
                    if ingredients_data and ingredient_data['name'] in [i['name'] for i in ingredients_data]:
                        ingredient_data.setdefault('unit', "Gram")
                        ingredient_data.setdefault('quantity', 1)
                        ingredient_model = Ingredient.objects.get(name=ingredient_data['name'])
                        unit_model = ingredient_model.units.get(name=ingredient_data['unit'])
                        recipe_model.ingredients.add(ingredient_model,
                                                     through_defaults={'quantity': ingredient_data['quantity'],
                                                                       'unit': unit_model})
                if 'tools' in recipe_data:
                    for tool_data in recipe_data['tools']:
                        assert 'name' in tool_data
                        if tools_data and tool_data['name'] in [t['name'] for t in tools_data]:
                            recipe_model.tools.add(CookingTool.objects.get(name=tool_data['name']))

    @classmethod
    def create_default_test_database(cls, *, units=False, ingredients=False, tools=False, recipes=False):
        if units:
            units_data = [
                {
                    'name': "Gram",
                    'amount': 1
                },
                {
                    'name': "Kilogram",
                    'amount': 10
                }
            ]
        else:
            units_data = None

        if ingredients:
            ingredients_data = [
                {
                    'name': "Woda",
                    'price': 2,
                    'is_vegetarian': False,
                    'is_vegan': False,
                    'is_gluten_free': True,
                    'units': [
                        {
                            'name': "Gram"
                        },
                        {
                            'name': "Kilogram"
                        }
                    ]
                },
                {
                    'name': "Cytryna",
                    'price': 8,
                    'is_vegetarian': True,
                    'is_vegan': False,
                    'is_gluten_free': False,
                    'units': [
                        {
                            'name': "Kilogram"
                        }
                    ]
                },
                {
                    'name': "Jabłko",
                    'price': 5,
                    'is_vegetarian': False,
                    'is_vegan': True,
                    'is_gluten_free': False,
                    'units': [
                        {
                            'name': "Gram"
                        }
                    ]
                }
            ]
        else:
            ingredients_data = None

        if tools:
            tools_data = [
                {
                    'name': "Patelnia"
                },
                {
                    'name': "Garnek"
                }
            ]
        else:
            tools_data = None

        if recipes:
            recipes_data = [
                {
                    'name': "Lemoniada",
                    'description': "Woda, ale słodka",
                    'recipe': "Domyśl się",
                    'ingredients': [
                        {
                            'name': "Woda",
                            'quantity': 1,
                            'unit': "Gram"
                        },
                        {
                            'name': "Cytryna",
                            'quantity': 2,
                            'unit': "Kilogram"
                        }
                    ],
                    'tools': [
                        {
                            'name': "Garnek"
                        }
                    ]
                }
            ]
        else:
            recipes_data = None
        cls.create_custom_test_database(units_data=units_data,
                                        tools_data=tools_data,
                                        ingredients_data=ingredients_data,
                                        recipes_data=recipes_data)
