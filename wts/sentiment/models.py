from __future__ import unicode_literals, division

from django.db import models


class Entity(models.Model):
    name = models.TextField(max_length=100)
    pos = models.IntegerField()
    tot = models.IntegerField()

    @property
    def pos_ratio(self):
        return float("{0:.2f}".format(100 * self.pos / self.tot))

    @property
    def pos_ratio_int(self):
        return int(self.ratio)

    @property
    def neg(self):
        return self.tot - self.pos

    @property
    def neg_ratio(self):
        return float("{0:.2f}".format(100 * self.neg / self.tot))

    class Meta:
        verbose_name_plural = "entities"
