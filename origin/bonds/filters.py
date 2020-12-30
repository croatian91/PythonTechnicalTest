from django_filters import rest_framework as filters

from .models import Bond


class BondFilter(filters.FilterSet):
    """
    Bond filter using FilterSet as a shortcut
    """

    min_size = filters.NumberFilter(field_name="size", lookup_expr="gte")
    max_size = filters.NumberFilter(field_name="size", lookup_expr="lte")
    maturity_range = filters.DateRangeFilter(field_name="maturity")

    class Meta:
        model = Bond
        fields = ["isin", "size", "currency", "maturity", "lei", "legal_name"]
