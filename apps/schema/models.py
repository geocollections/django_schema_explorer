
from django.db import models


class Agent(models.Model):
    agent = models.CharField(unique=True, max_length=150)
    forename = models.CharField(max_length=150, blank=True)
    surname = models.CharField(max_length=150, blank=True)
    title = models.CharField(max_length=60, blank=True)
    profession = models.CharField(max_length=150, blank=True)
    institution_name = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=300, blank=True)
    country = models.ForeignKey('ListCountry', null=True, db_column='country_id', blank=True)
    phone = models.CharField(max_length=60, blank=True)
    email = models.CharField(max_length=300, blank=True)
    webpage = models.CharField(max_length=300, blank=True)
    date_born = models.DateField(null=True, blank=True)
    date_deceased = models.DateField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    id = models.AutoField(primary_key=True, db_column='id')

    class Meta:
        db_table = 'agent'

    def __str__(self):
        return self.agent

class Analysis(models.Model):
    material = models.CharField(max_length=50, blank=True)
    id = models.AutoField(primary_key=True, db_column='id')
    sample = models.ForeignKey('Sample', db_column='sample_id')
    analysis_method = models.ForeignKey('AnalysisMethod', db_column='method', null=True)
    method_details = models.CharField(max_length=255, blank=True)
    mass = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    lab_txt = models.CharField(max_length=255, blank=True)
    lab_sample_number  = models.CharField(max_length=50, blank=True)
    lab_analysis_number  = models.CharField(max_length=50, blank=True)
    instrument_txt = models.CharField(max_length=255, blank=True)    
    agent = models.ForeignKey(Agent, null=True, blank=True)
    owner = models.ForeignKey(Agent, null=True, blank=True)
    remarks = models.TextField(blank=True)

    class Meta:
        db_table = 'analysis'

    def __str__(self):
        return self.id


class AnalysisMethod(models.Model):
    analysis_method = models.CharField(max_length=100, db_column='method')
    parent_method = models.ForeignKey('self', null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    id = models.AutoField(primary_key=True, db_column='id')

    class Meta:
        db_table = 'analysis_method'

    def __str__(self):
        return self.analysis_method

class ListCountry(models.Model):
    country = models.CharField(max_length=50, unique=True, blank=True)
    id = models.AutoField(primary_key=True, db_column='id')
    class Meta:
        db_table = 'list_country'
    def __str__(self):
        return self.value

class Locality(models.Model):
    locality = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, blank=True)
    parent_locality = models.ForeignKey('self', null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    elevation = models.DecimalField(decimal_places=6,max_digits=10, null=True, blank=True)
    coord_system = models.CharField(max_length=50, blank=True)
    country = models.ForeignKey(ListCountry, null=True, blank=True)
    depth = models.FloatField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    id = models.AutoField(primary_key=True, db_column='id')
    class Meta:
        db_table = 'locality'
    def __str__(self):
        return self.locality


class DbTables(models.Model):
    name = models.CharField()
    contents = models.CharField() 
    description = models.TextField(blank=True)
    id = models.AutoField(primary_key=True, db_column='id')
    class Meta:
        db_table = 'db_tables'
    def __str__(self):
        return self.name

class TableFields(models.Model):
    name = models.CharField()
    table = models.ForeignKey(DbTables, db_column='table_id')
    description = models.TextField(blank=True)
    id = models.AutoField(primary_key=True, db_column='id')
    class Meta:
        db_table = 'table_fields'
    def __str__(self):
        return self.name


class Sample(models.Model):
    number = models.CharField(max_length=60, blank=True)
    number_field = models.CharField(max_length=75, blank=True)
    parent_sample = models.ForeignKey('self', null=True, blank=True, db_column='parent_sample_id')
    locality = models.ForeignKey(Locality, null=True, blank=True)
    depth = models.FloatField(null=True, blank=True)
    depth_interval = models.FloatField(null=True, blank=True)
    agent_collected = models.ForeignKey(Agent, null=True, blank=True)
    date_collected = models.DateField(null=True, blank=True)
    rock = models.CharField(max_length=255, blank=True)
    analysed = models.BooleanField(null=True, blank=True)
    mass = models.IntegerField(null=True, blank=True)
    location = models.CharField(null=True, blank=True)
    remarks = models.TextField(blank=True,)
    owner = models.ForeignKey(Agent, null=True, blank=True, db_column='owner_id')
    id = models.AutoField(primary_key=True, db_column='id')

    class Meta:
        db_table = 'sample'

    def __str__(self):
        return self.number

