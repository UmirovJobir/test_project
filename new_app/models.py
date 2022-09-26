from django.db import models

class Country(models.Model):
    country_name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.country_name
    
    class Meta:
        verbose_name_plural = 'Countries'

class Product(models.Model):
    code_product = models.BigIntegerField()
    product_name = models.TextField()
    skp = models.CharField(max_length=50)
    # country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='test')

    # def current_epg(self):
    #     return Detail.objects.filter(product=self)

    def __str__(self):
        return self.product_name
    
    class Meta:
        verbose_name_plural = 'Products'
        # unique_together = ('code_product', 'country',)


class Detail(models.Model):
    price = models.FloatField(null=True, blank=True)
    duty = models.FloatField(null=True, blank=True)
    year = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='details')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='countries')

    def __str__(self):
        return f"{self.product} {self.year}"
    
    class Meta:
        verbose_name_plural = 'Details'







