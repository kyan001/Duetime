import random

from django.db import models
from django.forms.models import model_to_dict
from django.http import Http404


class BaseManager(models.Manager):
    def get_or_none(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            return None

    def get_or_404(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            raise Http404('您查找的 {t} 并不存在。（查询参数 {a} {k}）'.format(t=self.model.__name__, a=args or '', k=kwargs or ''))


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    objects = BaseManager()

    class Meta:
        abstract = True

    def toArray(self):
        self.created = self.created.isoformat(' ')
        self.modified = self.modified.isoformat(' ')
        return model_to_dict(self)


class CardnoteCard(BaseModel):
    CATEGORIES = (
        ('default', 'Default'),
        ('primary', 'Primary'),
        ('info', 'Info'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('danger', 'Danger'),
    )
    title = models.CharField(max_length=30)
    kcol = models.CharField(max_length=30, blank=True)
    vcol = models.CharField(max_length=30, blank=True)
    username = models.CharField(max_length=30, blank=True)
    category = models.CharField(max_length=20, blank=True, choices=CATEGORIES, default='default')

    def __str__(self):
        return "{self.id}. {self.title} ({self.kcol} / {self.vcol})".format(self=self)

    @property
    def cardnoteitems(self):
        return CardnoteItem.objects.filter(cardnotecardid=self.id)

    @property
    def last_updated(self):
        return self.cardnoteitems.order_by('-modified').get().modified


class CardnoteItem(BaseModel):
    cardnotecardid = models.IntegerField()
    kword = models.CharField(max_length=128, blank=True)
    val = models.CharField(max_length=512, blank=True)

    def __str__(self):
        return "{self.id}. ({self.cardnotecard.title}) {self.kword}: {self.val}".format(self=self)

    @property
    def cardnotecard(self):
        card = CardnoteCard.objects.get(id=self.cardnotecardid)
        return card
