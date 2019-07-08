from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import reverse

from vrl.datamodel.tests.factories import CommunicatieKanaalFactory


class CommunicatieKanaalTests(APITestCase):
    def test_list_and_detail(self):
        url = reverse("communicatiekanaal-list")
        for i in range(0, 20):
            CommunicatieKanaalFactory.create(naam=str(i))

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 20)
        self.assertIn("results", data)

        detail_url = data["results"][3]["url"]

        detail = self.client.get(detail_url)

        self.assertEqual(detail.status_code, status.HTTP_200_OK)
        self.assertEqual(detail.json(), data["results"][3])
