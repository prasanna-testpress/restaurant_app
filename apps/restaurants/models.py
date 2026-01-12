from django.db import models


class Cuisine(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Restaurant(models.Model):

    class VegChoices(models.TextChoices):
        VEG = "veg", "Veg"
        NON_VEG = "non_veg", "Non Veg"
        VEGAN = "vegan", "Vegan"

    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    address = models.TextField()

    cost_for_two = models.PositiveIntegerField()

    veg_type = models.CharField(
        max_length=10,
        choices=VegChoices,
    )

    cuisines = models.ManyToManyField(
        Cuisine,
        related_name="restaurants",
    )

    is_open = models.BooleanField(default=True)
    is_spotlight = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["city"]),
            models.Index(fields=["is_spotlight"]),
            models.Index(fields=["veg_type"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "city"],
                name="unique_restaurant_per_city",
            )
        ]

    def __str__(self):
        return self.name

    
    @property
    def cover_image(self):
        image = self.images.first()
        return image.image.url if image else None


class MenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="menu_items",
    )
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()

    image = models.ImageField(
        upload_to="menu_items/",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["restaurant", "name"],
                name="unique_menu_item_per_restaurant",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"


class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="restaurants/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
