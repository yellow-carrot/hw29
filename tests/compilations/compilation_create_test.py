import pytest

from tests.factories import AdFactory


@pytest.mark.django_db
def test_compilation_create(client, user_and_access_token):
    user, access_token = user_and_access_token
    ad_list = AdFactory.create_batch(3)

    data = {
        'name': 'test_compilation_name',
        'items': [ad.pk for ad in ad_list]
    }

    expected_data = {
        # 'id': 1,
        'name': 'test_compilation_name',
        'owner': user.username,
        # 'items': [ad.pk for ad in ad_list]
    }

    response = client.post('/compilation/', data=data, HTTP_AUTHORIZATION=f"Bearer {access_token}")

    assert response.status_code == 201
    assert response.data == expected_data
