from components.hero import render_hero
from utils import image_handler as ih


def render(t):
    render_hero(t)
    ih.photo_manager("cover", [t["cover"]["title"].title() + " — hero"], t)
