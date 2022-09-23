# Generated by Django 4.1.1 on 2022-09-22 15:14

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_rename_filter_categoryattribute_filter_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category_attributes',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.RemoveField(
            model_name='skucategoryattribute',
            name='product',
        ),
        migrations.CreateModel(
            name='StockKeepingUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recommended_retail_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('sale_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('in_stock', models.PositiveSmallIntegerField(default=0)),
                ('on_sale', models.BooleanField(default=False)),
                ('web_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('category_attributes', models.ManyToManyField(through='products.SKUCategoryAttribute', to='products.categoryattribute')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
        migrations.AddField(
            model_name='skucategoryattribute',
            name='sku',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='products.stockkeepingunit'),
            preserve_default=False,
        ),
    ]