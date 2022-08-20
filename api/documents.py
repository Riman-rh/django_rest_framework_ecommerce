from django_elasticsearch_dsl import fields, Document
from django_elasticsearch_dsl.registries import registry
import elasticsearch_dsl as dsl

from .models import Product, Review

TEXT_RAW = dsl.Text(fields={"raw": dsl.Keyword()})

'''
@registry.register_document
class ProductDocument(Document):
    class Index:
        name = 'products_1'

    class Django:
        model = Product
        fields = [
                  'id',
                  'name_ar',
                  'name_fr',
                  'name_en',
                  'photo',
                  'description',
                  'stock',
        ]


@registry.register_document
class ReviewDocument(Document):
    class Index:
        name = 'reviews'

    class Django:
        model = Review
        fields = [
            'id',
            'rating',
            'comment',
        ]
'''