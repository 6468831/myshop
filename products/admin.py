from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import *

class StockKeepingUnitID(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Product)
admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        # ...more fields if you feel like it...
    ),
    list_display_links=(
        'indented_title',
    ),)

admin.site.register(Attribute)
admin.site.register(CategoryAttribute)
admin.site.register(SKUCategoryAttribute)
admin.site.register(Image)
admin.site.register(StockKeepingUnit, StockKeepingUnitID)
admin.site.register(FileUpload)

