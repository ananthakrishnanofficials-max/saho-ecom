from django.contrib import admin

from django import template

from .models import Product, ProductImage, Order, Cart, Festival, Category, ProductFeature, ProductVariant, Review, SubCategory, Wishlist, PresentationBlock
register = template.Library()


class PresentationBlockInline(admin.StackedInline):
    model = PresentationBlock
    extra = 1

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    fields = ("size", "color", "stock", "extra_price")
    extra = 1

class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 3

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [PresentationBlockInline, ProductFeatureInline, ProductImageInline, ProductVariantInline]

    list_display = ("name","hero_title", "price", "sub_category", "get_category", "is_active","rating","is_bestseller","is_trending","original_price","festival")
    list_filter = ("sub_category","sub_category__parent_category", "is_active","is_bestseller","is_trending","festival",)
    search_fields = ("name", "description","hero_title","hero_description","original_price","rating","is_bestseller", "is_trending","festival__name")
    prepopulated_fields = {"slug": ("name",)}
    actions = ['mark_as_featured']
    
    def get_category(self, obj):
        return obj.sub_category.parent_category
    get_category.short_description = "Category"

    def mark_as_featured(self, request, queryset):
        queryset.update(featured=True)
    mark_as_featured.short_description = "Mark selected products as Featured"

@admin.register(PresentationBlock)
class PresentationBlockAdmin(admin.ModelAdmin):
    list_display = ("product", "title")  # adjust fields as needed


@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location','image')   


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "is_approved", "created_at")
    list_filter = ("rating", "is_approved")




# 🔹 Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "product_name", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("product_name", "user__username")


# 🔹 Cart Admin
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "quantity")
    list_filter = ("user",)

class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1

class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    inlines = [SubCategoryInline]
    prepopulated_fields = {"slug": ("name",)}

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_category', 'slug', 'tagline')
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    search_fields = ('user__username', 'product__name')