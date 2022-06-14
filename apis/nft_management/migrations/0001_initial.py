# Generated by Django 4.0.1 on 2022-01-24 12:02

import apis.nft_management.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_removed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('logo_image', models.ImageField(upload_to=apis.nft_management.models.upload_to)),
                ('banner_image', models.ImageField(upload_to=apis.nft_management.models.upload_to)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('is_removed', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collection_category', to='nft_management.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_collection', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('id',),
                'unique_together': {('name', 'user')},
            },
        ),
        migrations.CreateModel(
            name='Nft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to=apis.nft_management.models.upload_to)),
                ('royalty', models.FloatField(default=0.0)),
                ('size', models.TextField(null=True)),
                ('no_of_copies', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sale_type', models.CharField(choices=[('is_put_on_sale', 'Is Put On Sale'), ('is_instant_sale_price', 'Is Instant Sale Price'), ('is_unlock_purchase', 'Is Unlock Purchase')], max_length=40)),
                ('is_hidden', models.BooleanField(default=False)),
                ('is_removed', models.BooleanField(default=False)),
                ('total_views', models.IntegerField(default=0)),
                ('expiry_date', models.DateField(blank=True, null=True)),
                ('price', models.FloatField()),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nft_collection', to='nft_management.collection')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nft_owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('id',),
                'unique_together': {('name', 'owner')},
            },
        ),
        migrations.CreateModel(
            name='ReportedNft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_type', models.CharField(choices=[('fake', 'Fak or spam'), ('explicit', 'Explicit and Sensitive Content'), ('might_be_stolen', 'Might be Stolen'), ('other', 'Other')], max_length=40)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_resolved', models.BooleanField(default=False)),
                ('nft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reported_nft', to='nft_management.nft')),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reporter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NftPriceHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('nft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nft_history', to='nft_management.nft')),
            ],
        ),
        migrations.CreateModel(
            name='FavouriteNft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_favorite', models.BooleanField(default=True)),
                ('nft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourite_nft', to='nft_management.nft')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_favourite', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
