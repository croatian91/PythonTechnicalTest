from datetime import date

from rest_framework import serializers

from .models import Bond


class BondSerializer(serializers.ModelSerializer):
    legal_name = serializers.CharField(required=False)

    def validate_size(self, size):
        if size < 1:
            raise serializers.ValidationError("Only positive size accepted")
        return size

    def validate_currency(self, currency):
        if len(currency) != 3 or not currency.isupper():
            raise serializers.ValidationError("Currency must be 3 upper case letters")
        return currency

    def validate_maturity(self, maturity):
        if maturity <= date.today():
            raise serializers.ValidationError("Date must be in the future")
        return maturity

    class Meta:
        model = Bond
        exclude = ["id", "owner"]
