class Drink(object):
    def __init__(self, name, description, color, skill, isAlcoholic,
                 isCarbonated, isHot, ingredients, tastes, occasions, tools,
                 actions):
        self.name = name
        self.description = description
        self.color = color
        self.skill = skill
        self.isAlcoholic = isAlcoholic
        self.isCarbonated = isCarbonated
        self.isHot = isHot
        self.ingredients = ingredients
        self.tastes = tastes
        self.occasions = occasions
        self.tools = tools
        self.actions = actions

def createDrink(name, description, color, skill, isAlcoholic, isCarbonated,
                isHot, ingredients, tastes, occasions, tools, actions):
    return Drink(name, description, color, skill, isAlcoholic, isCarbonated,
        isHot, ingredients, tastes, occasions, tools, actions)
