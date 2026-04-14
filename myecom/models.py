from datetime import date
from django.contrib.auth.models import User
from django.db import models
from django import forms
from django.templatetags.static import static
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta
from django.db import models   # if Product is in the same app


class PresentationBlock(models.Model):
    product = models.ForeignKey(
        "Product",   # <-- string reference avoids circular import
        related_name="presentation_blocks",
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.titl

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Needs Pillow library installed via pip: pip install Pillow
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True) 
    
    display_name = models.CharField(max_length=50, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Optional: Add Django Signals here to auto-create a UserProfile 
# whenever a new User signs up.

class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='United States')
    
    delivery_instructions = models.TextField(blank=True, null=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.address_line_1}"

    def save(self, *args, **kwargs):
        # If this address is set as default, remove the default status from all others
        if self.is_default:
            UserAddress.objects.filter(user=self.user).update(is_default=False)
        super().save(*args, **kwargs)

class SahoPlusMembership(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='saho_plus')
    is_active = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    
    # Optional: Tracking stats for the "Savings" gamification section
    shipping_saved = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cashback_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Membership - {'Active' if self.is_active else 'Inactive'}"

    def activate_membership(self, duration_days=365):
        """Activates membership for a given number of days."""
        self.is_active = True
        self.start_date = timezone.now()
        self.end_date = timezone.now() + timedelta(days=duration_days)
        self.save()

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user} - {self.product}"


class Festival(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='festivals/', null=True, blank=True)
    
    def __str__(self):
        return self.name
    

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    parent_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    hero_image = models.ImageField(upload_to="subcategory_heroes/", blank=True, null=True)
    tagline = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.parent_category} → {self.name}"

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('homedecor', 'HomeDecor'),
        ('fashion', 'Fashion'),
        ('electronics', 'Electronics'),
        ('grocery', 'Grocery'),
        ('healthcare', 'Healthcare'),
        ('festival','Festival'),
        ('mobile', 'Mobile'),
    ]
    

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    price = models.IntegerField() 
    stock = models.PositiveIntegerField(null=True, blank=True)
  # safe fallback   # ✅ default avoids migration prompt
    rating = models.FloatField(default=0)
    original_price = models.IntegerField(null=True, blank=True)
    is_bestseller = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    sub_category = models.ForeignKey("SubCategory",on_delete=models.CASCADE,related_name="products",null=True,blank=True)

    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)

    hero_title = models.CharField(max_length=255, blank=True, null=True)
    hero_description = models.TextField(blank=True, null=True)
    hero_image = models.ImageField(upload_to='hero_images/', blank=True, null=True)
    festival = models.ForeignKey(
        Festival,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products"
    )

    def hero_image_url(self):
        if self.hero_image and hasattr(self.hero_image, 'url'):
            return self.hero_image.url
        return static("images/placeholder.jpg")

    def __str__(self):
      return self.name

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name="variants", on_delete=models.CASCADE)
    size = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    extra_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.product.name} - {self.size or ''} {self.color or ''}"
class ProductFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="features")

    title = models.CharField(max_length=100)   # Ultra Performance
    subtitle = models.CharField(max_length=200, blank=True)  # All-new technology
    description = models.TextField()
    image = models.ImageField(upload_to="features/")

    def __str__(self):
        return f"{self.product.name} - {self.title}"
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.product.name
    
    original_price = models.IntegerField(null=True, blank=True)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    rating = models.IntegerField()  # 1 to 5
    comment = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)  # for admin control
    

    class Meta:
        unique_together = ('product', 'user') 

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]

    def __str__(self):
        return f"{self.user} - {self.product}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    status = models.CharField(max_length=50, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.product_name}"
    
    
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

# change app name if different

