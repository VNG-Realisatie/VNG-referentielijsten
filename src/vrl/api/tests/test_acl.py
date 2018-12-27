from rest_framework.test import APITestCase
from zds_schema.tests import reverse

from vrl.datamodel.models import CommunicatieKanaal


class CommunicatieKanaalTests(APITestCase):

    def test_create_forbidden(self):
        url = reverse('communicatiekanaal-list')

        response = self.client.post(url, {
            'naam': 'foo',
            'omschrijving': 'bar'
        })

        self.assertGreater(response.status_code, 400)
        self.assertLess(response.status_code, 500)

    def test_update_forbidden(self):
        comm_kanaal = CommunicatieKanaal.objects.create(naam='telefoon', omschrijving='banana phone')
        url = reverse('communicatiekanaal-detail', kwargs={'uuid': comm_kanaal.uuid})

        response = self.client.put(url, {
            'naam': 'foo',
            'omschrijving': 'bar'
        })

        self.assertGreater(response.status_code, 400)
        self.assertLess(response.status_code, 500)

        response = self.client.patch(url, {
            'naam': 'foo',
            'omschrijving': 'bar'
        })

        self.assertGreater(response.status_code, 400)
        self.assertLess(response.status_code, 500)
