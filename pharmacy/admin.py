from django.contrib import admin
from .models import Pharmacy, Medicine, SearchHistory

# Pharmacy lo nundi Medicine link cheyadaniki
class MedicineInline(admin.TabularInline):
    model = Medicine.pharmacies.through
    extra = 1
    verbose_name = "Link Medicine"
    verbose_name_plural = "Link Medicines"

@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'highway', 'distance', 'phone', 'is_open_24', 'rating']
    list_filter = ['highway', 'is_open_24', 'rating']
    search_fields = ['name', 'location', 'phone']
    list_editable = ['is_open_24', 'rating']
    inlines = [MedicineInline]  # <-- Idi kothaga add chesanu

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_available']
    list_filter = ['category', 'is_available']
    search_fields = ['name', 'generic_name']
    filter_horizontal = ['pharmacies']

@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ['medicine_name', 'highway', 'user', 'searched_at']
    list_filter = ['highway']