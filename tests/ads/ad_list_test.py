import pytest

from ads.serializers import AdSerializer
from tests.factories import AdFactory


@pytest.mark.django_db
def test_ad_retrieve(client):
    ad_list = AdFactory.create_batch(2)

    response = client.get(f"/ad/")
    assert response.status_code == 200
    assert response.data == {"count": 2,
                             "next": None,
                             "previous": None,
                             "results": AdSerializer(ad_list, many=True).data
                             }
