from .models import Category
def menus(request):
    menu_item = Category.objects.filter(main_category=None)
    return dict(menu_item=menu_item)