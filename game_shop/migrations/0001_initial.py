# Generated by Django 3.2 on 2021-04-29 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('address', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'customer',
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=200)),
                ('Release_date', models.DateField(null=True)),
                ('Required_age', models.IntegerField(null=True)),
                ('achievements', models.BooleanField(null=True)),
                ('positive_ratings', models.IntegerField(null=True)),
                ('negative_ratings', models.IntegerField(null=True)),
                ('average_playtime', models.IntegerField(null=True)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Genres',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Platforms',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_shop.customer')),
            ],
        ),
        migrations.CreateModel(
            name='LineItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_shop.cart')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_shop.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_shop.game')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='Genres',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='game_shop.genres'),
        ),
        migrations.AddField(
            model_name='game',
            name='Platforms',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='game_shop.platforms'),
        ),
        migrations.AddField(
            model_name='game',
            name='Publisher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='game_shop.publisher'),
        ),
        migrations.AddField(
            model_name='cart',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_shop.game'),
        ),
    ]
