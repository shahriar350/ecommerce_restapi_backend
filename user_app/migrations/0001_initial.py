# Generated by Django 3.2.5 on 2021-07-23 13:31

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('seller_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(null=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_cart', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('completed', models.BooleanField(default=False)),
                ('cart', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart_checkout', to='user_app.cart')),
            ],
        ),
        migrations.CreateModel(
            name='UserLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.CharField(blank=True, max_length=150, null=True)),
                ('street', models.CharField(blank=True, max_length=150, null=True)),
                ('house', models.CharField(blank=True, max_length=150, null=True)),
                ('post_office', models.CharField(blank=True, max_length=150, null=True)),
                ('post_code', models.CharField(blank=True, max_length=10, null=True)),
                ('police_station', models.CharField(blank=True, max_length=150, null=True)),
                ('city', models.CharField(blank=True, max_length=150, null=True)),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_locations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CheckoutProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(editable=False)),
                ('selling_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('offer_price', models.PositiveIntegerField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('quantity', models.PositiveIntegerField(blank=True, default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('received', models.BooleanField(default=False)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Order placed'), (1, 'Processing'), (2, 'Packaging'), (3, 'On-way'), (4, 'Reached'), (5, 'Completed')], default=0)),
                ('checkout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checkout_products', to='user_app.checkout')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_checkouts', to='seller_app.product')),
            ],
        ),
        migrations.AddField(
            model_name='checkout',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location_checkouts', to='user_app.userlocation'),
        ),
        migrations.AddField(
            model_name='checkout',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_checkouts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('cart', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart_products', to='user_app.cart')),
                ('product', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_cart', to='seller_app.product')),
                ('variation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart_product_variations', to='seller_app.productvariance')),
            ],
        ),
    ]
