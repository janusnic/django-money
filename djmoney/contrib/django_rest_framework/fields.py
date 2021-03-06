# coding: utf-8
from moneyed import Money
from rest_framework.serializers import DecimalField, ModelSerializer

from djmoney.models.fields import MoneyField as ModelField

from .helpers import IS_DRF_3


class MoneyField(DecimalField):
    """
    Treats ``Money`` objects as decimal values in representation and
    does decimal's validation during transformation to native value.
    """

    if IS_DRF_3:

        def to_representation(self, obj):
            return super(MoneyField, self).to_representation(obj.amount)

        def to_internal_value(self, data):
            if isinstance(data, Money):
                amount = super(MoneyField, self).to_internal_value(data.amount)
                return Money(amount, data.currency)
            return super(MoneyField, self).to_internal_value(data)

    else:

        def to_native(self, value):
            amount = value.amount if isinstance(value, Money) else value
            return super(MoneyField, self).to_native(amount)

        def from_native(self, value):
            if isinstance(value, Money):
                amount = super(MoneyField, self).from_native(value.amount)
                return Money(amount, value.currency)
            return super(MoneyField, self).from_native(value)

        def validate(self, value):
            amount = value.amount if isinstance(value, Money) else value
            return super(MoneyField, self).validate(amount)


def register_money_field():
    mapping = ModelSerializer.serializer_field_mapping if IS_DRF_3 else ModelSerializer.field_mapping
    mapping[ModelField] = MoneyField
