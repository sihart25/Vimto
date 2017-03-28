from django.db import models


#class Model_Sensor(models.Model): 
#    name = models.CharField(max_length=50)
#
#    def __str__(self):
#        return self.name
#
#    class Meta:
#        ordering = ['name']


#class Model_Sensor(models.Model):
#    name = models.CharField(max_length=50)
#
#    def __str__(self):
#        return self.name
#
#    class Meta:
#        ordering = ['name']

#
#class Model_Section(models.Model):
#
#    name = models.CharField(max_length=50)
#    section_direction = models.CharField(max_length=1, choices = SENSORS)
#    minlat = models.FloatField()
#    minlng = models.FloatField()
#    maxlat = models.FloatField()
#    maxlng = models.FloatField()
#    startlat = models.FloatField()
#    startlng = models.FloatField()
#    endlat = models.FloatField()
#    endlng = models.FloatField()
#
#    def __str__(self):
#        return self.name
#
#    class Meta:
#        ordering = ['name']


#class Model_file(models.Model):
#    description_text = models.CharField(max_length=200)
#    choice_text = models.CharField(max_length=200)
#    votes = models.IntegerField(default=0)
#    pub_date = models.DateTimeField('date created')

#
#class Model_DataforSection(models.Model):
#    name = models.CharField(max_length=50)
#    parentfile = models.CharField(max_length=50)
#
#    mySection = models.ForeignKey(
#        Model_Section,
#        on_delete=models.CASCADE,
#        verbose_name="the related Model_Section",
#    )
#
#
#    Model_Sensor = models.OneToOneField(
#        Model_Sensor,
#        on_delete=models.CASCADE,
#        verbose_name="related Sensor",
#    )
#
#    def __str__(self):
#        return self.name
#
#    class Meta:
#        ordering = ['name']


class Model_MyCelModel(models.Model):
    fn = models.CharField(max_length=255)
    ln = models.CharField(max_length=255)

    def __unicode__(self):
        return "MyModel<%s, %s>" % (self.fn, self.ln)


class Color(models.Model):
    """
    The color's name (as used by the CSS 'color' attribute, meaning
    lowercase values are required), and a boolean of whether it's "liked"
    or not. There are NO USERS in this demo webapp, which is why there's no
    link/ManyToManyField to the User table.

    This implies that the website is only useable for ONE USER. If multiple
    users used it at the same time, they'd be all changing the same values
    (and would see each others' changes when they reload the page).
    """
    name = models.CharField(max_length=20)
    is_favorited = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class CalendarApp(models.Model):
    name = models.CharField(max_length=20) 
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

