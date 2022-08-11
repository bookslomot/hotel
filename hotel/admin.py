from django.contrib import admin

from hotel.models import Room, Visitor, Gym, Review, ApplicationForRoomBron


class ReviewVisitorsInRoom(admin.TabularInline):
    model = Visitor
    extra = 0
    fields = ('online_client', 'first_name', 'last_name', 'phone', )
    readonly_fields = ('online_client', 'first_name', 'last_name', 'phone',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'category', 'price', 'number_of_places', )
    search_fields = ('number',)
    ordering = ('number',)
    readonly_fields = ('price',)
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


@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('owner', 'created_at', 'active', 'rating')
    ordering = ('created_at',)
    search_fields = ('owner', 'rating',)
    list_editable = ('active',)
    list_filter = ('rating',)


@admin.register(ApplicationForRoomBron)
class ApplicationForBronAdmin(admin.ModelAdmin):

    list_display = ('user', 'room', 'status',)
    search_fields = ('user', 'room',)
    list_filter = ('status',)
    list_editable = ('status',)
    readonly_fields = ('user', 'room',)
