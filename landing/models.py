from django.db import models

class Subscriber(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=128)

    def __str__(self):
        # Чтобы вывести в качестве имени 2 поля
        return "Пользователь: %s --- %s" % (self.name, self.email)

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
