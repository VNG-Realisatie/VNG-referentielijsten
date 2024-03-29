from dateutil.relativedelta import relativedelta
from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import reverse

from vrl.selectielijst.tests.factories import ProcesTypeFactory, ResultaatFactory


class ProcesTypeTests(APITestCase):
    def test_lijst_procestypen(self):
        url = reverse("procestype-list")
        ProcesTypeFactory.create_batch(5)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(len(response_data), 5)

        # assert we can follow urls
        detail_url = response_data[2]["url"]

        detail = self.client.get(detail_url)

        self.assertEqual(detail.status_code, status.HTTP_200_OK)

    def test_lijst_resultaten(self):
        url = reverse("resultaat-list")
        resultaat1, resultaat2 = ResultaatFactory.create_batch(2)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 2)
        self.assertIn("url", response_data["results"][0])

    def test_filter_procestype(self):
        url = reverse("resultaat-list")
        resultaat1, resultaat2 = ResultaatFactory.create_batch(2)
        procestype_url = reverse(
            "procestype-detail", kwargs={"uuid": resultaat2.proces_type.uuid}
        )

        response = self.client.get(
            url, {"proces_type": f"http://testserver{procestype_url}"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)
        self.assertIn("url", response_data["results"][0])
        self.assertEqual(
            response_data["results"][0]["procesType"],
            f"http://testserver{procestype_url}",
        )

    def test_filter_procestype_by_jaar(self):
        url = reverse("procestype-list")
        procestype1 = ProcesTypeFactory.create(jaar=2017)
        procestype2 = ProcesTypeFactory.create(jaar=2018)

        response = self.client.get(url, {"jaar": 2017})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(len(response_data), 1)
        self.assertEqual(
            response_data[0]["url"],
            f"http://testserver{reverse(procestype1)}",
        )
        self.assertEqual(
            response_data[0]["jaar"],
            2017,
        )


class ResultaatTests(APITestCase):
    def test_get_resultaat(self):
        """
        test resultaat get api:
        bewaartermijn is displayed correctly
        procestermijn_opmerking is displayed correctly
        """
        resultaat = ResultaatFactory.create(
            bewaartermijn=relativedelta(years=10),
            procestermijn_opmerking="5 of 10 jaar",
        )
        url = reverse("resultaat-detail", kwargs={"uuid": resultaat.uuid})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["bewaartermijn"], "P10Y")
        self.assertEqual(response_data["procestermijnOpmerking"], "5 of 10 jaar")
