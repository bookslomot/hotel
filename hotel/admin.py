from django.contrib import admin

from hotel.models import Room, Visitor, Gym


class ReviewVisitorsInRoom(admin.TabularInline):
    model = Visitor
    extra = 0
    fields = ('online_client', 'first_name', 'last_name', 'phone', )
    readonly_fields = ('online_client', 'first_name', 'last_name', 'phone',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'category', 'price', 'number_of_places', 'free')
    list_filter = ('free',)
    search_fields = ('number',)
    ordering = ('number',)
    list_editable = ('free',)
    readonly_fields = ('price', 'visitors',)
    autocomplete_fields = ('visitors',)
    inlines = [ReviewVisitorsInRoom]
    save_on_top = True


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('id', 'online_client', 'adult', 'in_hotel')
    list_filter = ('adult', 'in_hotel')
    search_fields = ('last_name', 'first_name',)
    list_editable = ('adult', 'in_hotel')
    readonly_fields = ('in_hotel', 'gym')
    autocomplete_fields = ('number_room',)


@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    list_display = ('id', 'period', 'price', 'data_start', 'data_end')
    ordering = ('data_start', 'data_end',)
    readonly_fields = ('price', 'data_end', 'data_start')
    autocomplete_fields = ('visitor',)


