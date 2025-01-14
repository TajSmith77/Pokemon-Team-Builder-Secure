from django.contrib import admin
from .models import *
# Register your models here.

class PokemonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Pokemon, PokemonAdmin)
admin.site.register(Team, PokemonAdmin)
admin.site.register(Type, PokemonAdmin)
admin.site.register(Ability, PokemonAdmin)
admin.site.register(Move, PokemonAdmin)

