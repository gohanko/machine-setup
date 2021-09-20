import argparse
import colorama
from machine_setup.common import load_yaml
from machine_setup.recipe_parser import RecipeParser

if __name__ == '__main__':
    colorama.init()

    parser = argparse.ArgumentParser()
    parser.add_argument('recipe', help='Recipe/Instructions for setting up your machine.')

    args = parser.parse_args()
    if args.recipe:
        recipe = load_yaml(args.recipe)
        RecipeParser(recipe).run()