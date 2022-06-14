from accounts.models import User
from django.db import models


def upload_to(instance, filename):
    return 'posts/{filename}'.format(filename=filename)


choices = [
    ("is_put_on_sale", "Is Put On Sale"),
    ("is_instant_sale_price", "Is Instant Sale Price"),
    ("is_unlock_purchase", "Is Unlock Purchase")
]


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class Collection(models.Model):
    name = models.CharField(max_length=200)
    logo_image = models.ImageField(upload_to=upload_to)
    banner_image = models.ImageField(upload_to=upload_to)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    category = models.ForeignKey(Category, related_name="collection_category", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="user_collection", on_delete=models.CASCADE)
    is_removed = models.BooleanField(default=False)

    class Meta:
        ordering = ('id',)
        unique_together = ('name', 'user',)

    def __str__(self):
        return self.name


class Nft(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_to)
    royalty = models.FloatField(default=0.0)
    size = models.TextField(null=True)
    no_of_copies = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sale_type = models.CharField(max_length=40, choices=choices)
    is_hidden = models.BooleanField(default=False)
    is_removed = models.BooleanField(default=False)
    collection = models.ForeignKey(Collection, related_name="nft_collection", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name="nft_owner", on_delete=models.CASCADE)
    total_views = models.IntegerField(default=0)
    expiry_date = models.DateField(null=True,blank=True)

    price = models.FloatField()

    class Meta:
        ordering = ('id',)
        unique_together = ('name', 'owner',)

    def __str__(self):
        return self.name


class NftPriceHistory(models.Model):
    nft = models.ForeignKey(Nft, related_name="nft_history", on_delete=models.CASCADE)
    price = models.FloatField()
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nft}"


class FavouriteNft(models.Model):
    user = models.ForeignKey(User, related_name="user_favourite", on_delete=models.CASCADE)
    nft = models.ForeignKey(Nft, related_name="favourite_nft", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_favorite = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user} : {self.nft}"


class ReportedNft(models.Model):
    nft = models.ForeignKey(Nft, related_name="reported_nft", on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, related_name="reporter", on_delete=models.CASCADE)
    choices = [
        ("fake", "Fak or spam"),
        ("explicit", "Explicit and Sensitive Content"),
        ("might_be_stolen", "Might be Stolen"),
        ('other', 'Other')
    ]
    report_type = models.CharField(max_length=40, choices=choices)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_resolved = models.BooleanField(default=False)

    def delete(self, using=None, keep_parents=False):
        self.is_resolved = True
        return self.save()

    def __str__(self):
        return f"{self.nft}:  {self.reporter}"
