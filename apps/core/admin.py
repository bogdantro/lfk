from django.contrib import admin
from django.utils.html import format_html
from .models import Player, Sponsor, Team


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ("logo_preview", "name", "website", "is_active")
    list_editable = ("is_active",)

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="height:40px;border-radius:4px;" />',
                obj.logo.url
            )
        return "-"
    logo_preview.short_description = "Logo"


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = (
        "image_preview",
        "jersey_number",
        "first_name",
        "last_name",
        "position",
        "age",
        "team",
        "is_active",
    )

    list_filter = ("team", "position", )
    search_fields = ("first_name", "last_name", "jersey_number")
    ordering = ("team", "jersey_number")


    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:50px;width:50px;object-fit:cover;border-radius:6px;" />',
                obj.image.url
            )
        return "-"
    image_preview.short_description = "Bilde"