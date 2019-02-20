from django.db import models

# Create your models here.

class send_string(models.Model):
	input_str = models.CharField(max_length=512)

	class Meta:
		db_table= 'send_str'
