from abc import ABC, abstractmethod
import json


def parse_bool(value):
    if value == "true" or value == "on":
        return True
    elif value == "false" or value == "off":
        return False
    raise ValueError


class FormatController:
    def __init__(self, converter_type):
        self.converter = None
        self.set_converter_type(converter_type)

    def set_converter_type(self, converter_type):
        if converter_type == "json":
            self.converter = JsonFormatConverter()
        elif converter_type == "xml":
            self.converter = XmlFormatConverter()
        else:
            raise ValueError


class AbstractFormatConverter(ABC):
    @abstractmethod
    def convert_recipe_list(self, recipes):
        pass

    @abstractmethod
    def convert_full_recipe(self, recipes):
        pass

    @abstractmethod
    def convert_food_type_list(self, food_types, for_recipes):
        pass

    @abstractmethod
    def convert_recipe_ingredients(self, recipe_ingredients):
        pass

    @abstractmethod
    def convert_ingredient_list(self, ingredients):
        pass

    @abstractmethod
    def convert_preparation_step_list(self, step):
        pass


class JsonFormatConverter(AbstractFormatConverter):
    def convert_recipe_list(self, recipes):
        rep = list(
            map(lambda re: {"recipe_id": re.recipe_id, "name": re.name, "image": re.image, "rating": re.get_rating()},
                recipes))
        return json.dumps(rep, ensure_ascii=False)

    def convert_full_recipe(self, recipe):
        if recipe.is_author_anonymous:
            author = "anonymous"
        else:
            author = recipe.author.nickname
        return json.dumps({
            "recipe_id": recipe.recipe_id,
            "name": recipe.name,
            "author": author,
            "image": recipe.image,
            "preparation_in_minutes": recipe.preparation_in_minutes,
            "servings": recipe.servings,
            "difficulty": recipe.difficulty.title,
            "is_vegetarian": recipe.is_vegetarian,
            "is_vegan": recipe.is_vegan,
            "is_lactose_free": recipe.is_lactose_free,
            "is_gluten_free": recipe.is_gluten_free,
            "rating": recipe.get_rating(),
            "ingredients": self.convert_recipe_ingredients(recipe.ingredients),
            "preparation_steps": self.convert_preparation_step_list(recipe.steps),
            "food_types": self.convert_food_type_list(recipe.food_types, True)
        }, ensure_ascii=False)

    def convert_food_type_list(self, food_types, for_recipes):
        result = list(map(lambda ft: {"name": ft.name}, food_types))
        if for_recipes:
            return result
        return json.dumps(result, ensure_ascii=False)

    def convert_recipe_ingredients(self, ingredients):
        return list(map(lambda ing: {"name": ing.ingredient.name, "value": ing.value, "unit": ing.unit}, ingredients))

    def convert_preparation_step_list(self, steps):
        return list(map(lambda st: {"number": st.number, "text": st.text}, steps))

    def convert_ingredient_list(self, ingredients):
        return json.dumps(list(map(lambda ing: {"name": ing.name}, ingredients)), ensure_ascii=False)


class XmlFormatConverter(AbstractFormatConverter):
    def convert_recipe_list(self, recipes):
        xml_output = "<recipes>"
        for recipe in recipes:
            xml_output += f"<recipe recipe_id='{recipe.recipe_id}'>"
            xml_output += f"<name>{recipe.name}</name>"
            xml_output += f"<image>{recipe.image}</image>"
            xml_output += f"<rating>{recipe.get_rating()}</rating>"
            xml_output += "</recipe>"
        xml_output += "</recipes>"
        return xml_output

    def convert_full_recipe(self, recipe):
        if recipe.is_author_anonymous:
            author = "anonymous"
        else:
            author = recipe.author.nickname

        xml_output = f"<recipe recipe_id='{recipe.recipe_id}'>"
        xml_output += f"<name>{recipe.name}</name>"
        xml_output += f"<author>{author}</author>"
        xml_output += f"<image>{recipe.image}</image>"
        xml_output += f"<preparation_in_minutes>{recipe.preparation_in_minutes}</preparation_in_minutes>"
        xml_output += f"<servings>{recipe.servings}</servings>"
        xml_output += f"<difficulty>{recipe.difficulty.title}</difficulty>"
        xml_output += f"<is_vegetarian>{recipe.is_vegetarian}</is_vegetarian>"
        xml_output += f"<is_vegan>{recipe.is_vegan}</is_vegan>"
        xml_output += f"<is_lactose_free>{recipe.is_lactose_free}</is_lactose_free>"
        xml_output += f"<is_gluten_free>{recipe.is_gluten_free}</is_gluten_free>"
        xml_output += f"<rating>{recipe.get_rating()}</rating>"
        xml_output += self.convert_recipe_ingredients(recipe.ingredients)
        xml_output += self.convert_preparation_step_list(recipe.steps)
        xml_output += self.convert_food_type_list(recipe.food_types, True)
        xml_output += f"</recipe>"

        return xml_output

    def convert_food_type_list(self, food_types, for_recipes):
        xml_output = "<food_types>"
        for ft in food_types:
            xml_output += f"<food_type>"
            xml_output += f"<name>{ft.name}</name>"
            xml_output += f"</food_type>"
        xml_output = "</food_types>"
        return xml_output

    def convert_recipe_ingredients(self, ingredients):
        xml_output = "<ingredients>"
        for ing in ingredients:
            xml_output += f"<ingredient>"
            xml_output += f"<name>{ing.ingredient.name}</name>"
            xml_output += f"<value>{ing.value}</value>"
            xml_output += f"<unit>{ing.unit}</unit>"
            xml_output += f"</ingredient>"
        xml_output = "</ingredients>"
        return xml_output

    def convert_preparation_step_list(self, steps):
        xml_output = "<preparation_steps>"
        for st in steps:
            xml_output += f"<preparation_step>"
            xml_output += f"<number>{st.number}</number>"
            xml_output += f"<text>{st.text}</text>"
            xml_output += f"</preparation_step>"
        xml_output = "</preparation_steps>"
        return xml_output

    def convert_ingredient_list(self, ingredients):
        xml_output = "<ingredients>"
        for ing in ingredients:
            xml_output += f"<ingredient>"
            xml_output += f"<name>{ing.ingredient.name}</name>"
            xml_output += f"</ingredient>"
        xml_output = "</ingredients>"
        return xml_output
