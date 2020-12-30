from datetime import date
from unittest import mock

from django.contrib.auth.models import User
from freezegun import freeze_time
from rest_framework.reverse import reverse
from rest_framework.test import APISimpleTestCase, APITestCase

from .models import Bond


class HelloWorld(APISimpleTestCase):
    def test_root(self):
        resp = self.client.get("/")
        assert resp.status_code == 200


class TestBond(APITestCase):
    fixtures = ["users", "bonds"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.get_base_url = reverse("bonds-list")
        cls.user1 = User.objects.get(username="test")
        cls.user2 = User.objects.get(username="test2")

    def test_get_bonds_unauthenticated(self):
        """
        Test user unauthenticated
        """
        resp = self.client.get(self.get_base_url)
        assert resp.status_code == 401

    def test_get_bonds_user1(self):
        """
        Test without filter
        """
        self.client.force_authenticate(user=self.user1)
        resp = self.client.get(self.get_base_url)
        assert resp.status_code == 200
        assert len(resp.data) == 1
        assert resp.data[0]["lei"] == "R0MUWSFPU8MPRO8K5P83"

    def test_get_bonds_filters_gt(self):
        """
        Test gt filter for size attribute
        """
        self.client.force_authenticate(user=self.user2)
        urls = [
            "%s?min_size=100000002" % self.get_base_url,
            "%s?min_size=100000001" % self.get_base_url,
            "%s?min_size=100000000" % self.get_base_url,
        ]

        for i, url in enumerate(urls):
            resp = self.client.get(url)
            assert resp.status_code == 200
            assert len(resp.data) == i

    def test_get_bonds_filters_lt(self):
        """
        Test lt filter for size attribute
        """
        self.client.force_authenticate(user=self.user2)
        urls = [
            "%s?max_size=10" % self.get_base_url,
            "%s?max_size=100000000" % self.get_base_url,
            "%s?max_size=100000001" % self.get_base_url,
        ]

        for i, url in enumerate(urls):
            resp = self.client.get(url)
            assert resp.status_code == 200
            assert len(resp.data) == i

    def test_get_bonds_filters_eq(self):
        """
        Test equality filter for each attribute
        """
        self.client.force_authenticate(user=self.user2)
        urls = [
            "%s?isin=FR0000131105" % self.get_base_url,
            "%s?size=100000000" % self.get_base_url,
            "%s?currency=EUR" % self.get_base_url,
            "%s?maturity=2025-02-28" % self.get_base_url,
            "%s?lei=R0MUWSFPU8MPRO8K5P84" % self.get_base_url,
            "%s?legal_name=LCL" % self.get_base_url,
        ]

        for url in urls:
            resp = self.client.get(url)
            assert resp.status_code == 200
            assert len(resp.data) == 1

        url = "%s?isin=notgood" % self.get_base_url
        resp = self.client.get(url)
        assert resp.status_code == 200
        assert len(resp.data) == 0

    def test_get_bonds_unknown_filter(self):
        """
        Test unknown filter
        """
        self.client.force_authenticate(user=self.user2)
        url = "%s?unknown=val" % self.get_base_url
        resp = self.client.get(url)
        assert resp.status_code == 200
        assert len(resp.data) == 2

    def test_get_bonds_filter_maturity_range(self):
        """
        Test maturity range filter
        """
        self.client.force_authenticate(user=self.user2)
        url = "%s?maturity_range=today" % self.get_base_url
        with freeze_time("2025-02-28"):
            resp = self.client.get(url)
        assert resp.status_code == 200
        assert len(resp.data) == 1
        assert resp.data[0]["lei"] == "R0MUWSFPU8MPRO8K5P84"

        with freeze_time("2025-02-27"):
            resp = self.client.get(url)
        assert resp.status_code == 200
        assert len(resp.data) == 0

        url = "%s?maturity_range=year" % self.get_base_url
        with freeze_time("2025-01-01"):
            resp = self.client.get(url)
        assert resp.status_code == 200
        assert len(resp.data) == 1
        assert resp.data[0]["lei"] == "R0MUWSFPU8MPRO8K5P84"

    def test_post_bond_unauthenticated(self):
        """
        Test POST bond when unauthenticated
        """
        resp = self.client.post("/bonds/", {})
        assert resp.status_code == 401

    def test_post_bond(self):
        """
        Test POST bond when authenticated
        """
        self.client.force_authenticate(user=self.user1)
        data = {
            "isin": "EXAMPLE",
            "size": 100000000,
            "currency": "EUR",
            "maturity": "2025-02-28",
            "lei": "EXAMPLE",
            "legal_name": "EXAMPLE",
        }
        resp = self.client.post("/bonds/", data)
        bonds = Bond.objects.filter(isin="EXAMPLE")
        assert resp.status_code == 201
        assert len(bonds) == 1
        assert bonds[0].owner.pk == 1

    def test_post_bond_invalid_size(self):
        """
        Test POST bond with invalid size value
        """
        self.client.force_authenticate(user=self.user1)
        data = {
            "isin": "EXAMPLE",
            "size": -1,
            "currency": "EUR",
            "maturity": "2025-02-28",
            "lei": "EXAMPLE",
            "legal_name": "EXAMPLE",
        }
        resp = self.client.post("/bonds/", data)
        assert resp.data["size"][0] == "Only positive size accepted"
        assert resp.status_code == 400

    def test_post_bond_invalid_currency(self):
        """
        Test POST bond with invalid currency value
        """
        self.client.force_authenticate(user=self.user1)
        data = [
            {
                "isin": "EXAMPLE",
                "size": 100000000,
                "currency": "EuR",
                "maturity": "2025-02-28",
                "lei": "EXAMPLE",
                "legal_name": "EXAMPLE",
            },
            {
                "isin": "EXAMPLE",
                "size": 100000000,
                "currency": "EU",
                "maturity": "2025-02-28",
                "lei": "EXAMPLE",
                "legal_name": "EXAMPLE",
            },
        ]

        for d in data:
            resp = self.client.post("/bonds/", d)
            assert resp.data["currency"][0] == "Currency must be 3 upper case letters"
            assert resp.status_code == 400

    def test_post_bond_gleif_api_valid(self):
        pass

    @mock.patch("bonds.models.get_legal_name")
    def test_api(self, mock_get):
        """
        Test legal_name retrieved in signal from API and saved if not defined
        """
        self.client.force_authenticate(user=self.user2)
        mock_get.return_value = "BNP PARIBAS"
        lei = "R0MUWSFPU8MPRO8K5P83"
        # "legal_name" ommited to trigger API call
        data = {
            "isin": "EXAMPLE",
            "size": 100000000,
            "currency": "EUR",
            "maturity": "2025-02-28",
            "lei": lei,
        }
        resp = self.client.post("/bonds/", data)
        bond = Bond.objects.get(
            lei="R0MUWSFPU8MPRO8K5P83",
            legal_name=mock_get.return_value,
            owner=self.user2,
        )
        mock_get.assert_called_once_with(lei)
        assert resp.status_code == 201
        assert bond is not None
