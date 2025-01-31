from django.contrib import admin
from . models import Hotel_Model, HotelImage_Model, Room_Model, RoomImage_Model
# Register your models here.


class HotelImage_Inline(admin.TabularInline):
    model = HotelImage_Model
    extra = 5


class RoomImage_Inline(admin.TabularInline):
    model = RoomImage_Model
    extra = 5


class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country', 'total_rooms')
    inlines = [HotelImage_Inline]



class RoomAdmin(admin.ModelAdmin):
    list_display = ('get_hotel_name', 'room_type', 'available_rooms')
    inlines = [RoomImage_Inline]

    def get_hotel_name(self, obj):
        return obj.hotel.name

    get_hotel_name.short_description = 'Hotel Name'



admin.site.register(Hotel_Model, HotelAdmin)
admin.site.register(Room_Model, RoomAdmin)

