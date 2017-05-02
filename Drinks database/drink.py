class Drink(object):
    def __init__(self, name, description, color, skill, is_alcoholic,
                 is_carbonated, is_hot, ingredients, tastes, occasions, tools,
                 actions):
        self.name = name
        self.description = description
        self.color = color
        self.skill = skill
        self.is_alcoholic = is_alcoholic
        self.is_carbonated = is_carbonated
        self.is_hot = is_hot
        self.ingredients = ingredients
        self.tastes = tastes
        self.occasions = occasions
        self.tools = tools
        self.actions = actions

def create_drink(name, description, color, skill, is_alcoholic, is_carbonated,
                is_hot, ingredients, tastes, occasions, tools, actions):
    return Drink(name, description, color, skill, is_alcoholic, is_carbonated,
        is_hot, ingredients, tastes, occasions, tools, actions)
