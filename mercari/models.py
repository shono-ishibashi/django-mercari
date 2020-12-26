from django.db import models


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'


class ClosureTreeCategory(models.Model):
    closure_tree_category_id = models.AutoField(primary_key=True)
    ancestor = models.ForeignKey(
        Category, models.DO_NOTHING, db_column='ancestor',
        related_name='ancestor_category')
    descendant = models.ForeignKey(
        Category, models.DO_NOTHING, db_column='descendant',
        related_name='descendant_category')
    depth = models.IntegerField(blank=True, null=True)
    parent = models.ForeignKey(
        'self', models.DO_NOTHING, db_column='parent', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'closure_tree_category'


class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    condition = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(
        ClosureTreeCategory, models.DO_NOTHING, db_column='category',
        blank=True, null=True)
    brand = models.CharField(max_length=255, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    shipping = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'items'


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    mail_address = models.TextField()
    password = models.TextField()

    class Meta:
        managed = False
        db_table = 'users'
