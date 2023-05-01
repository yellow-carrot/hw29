import pytest

from ads.serializers import AdSerializer
from tests.factories import AdFactory


@pytest.mark.django_db
def test_ad_retrieve(client, access_token):
    ad = AdFactory.create()
    response = client.get(f"/ad/{ad.pk}/", HTTP_AUTHORIZATION=f"Bearer {access_token}")
    # print(response)
    assert response.status_code == 200
    assert response.data == AdSerializer(ad).data
