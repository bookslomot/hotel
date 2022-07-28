from django.contrib import admin

from hotel.models import Room, Visitor, Gym


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'category', 'price', 'number_of_places', 'free')
    list_filter = ('free',)
    search_fields = ('number',)
    ordering = ('number',)
    list_editable = ('free',)
    readonly_fields = ('price',)


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('id', 'online_client', 'adult', 'in_hotel')
    list_filter = ('adult', 'in_hotel')
    list_editable = ('adult', 'in_hotel')


@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    list_display = ('id', 'period', 'price', 'data_start', 'data_end')
    ordering = ('data_start', 'data_end',)
    readonly_fields = ('price', 'data_end', 'data_start')


