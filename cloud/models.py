# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Filepath(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20,blank=True,null=True)
    filename = models.CharField(max_length=100, blank=True, null=True)
    filetype = models.CharField(max_length=100, blank=True, null=True)
    viewtype = models.CharField(max_length=100,blank=True,null=True)
    uploaddate = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'filepath'


class User(models.Model):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, blank=True, null=True)
    passwd = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user'
