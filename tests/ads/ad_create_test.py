import pytest


@pytest.mark.django_db
def test_ad_create(client, user, category, access_token):

    data = {
        'name': 'test_ad_name',
        'price': 111,
        'author_id': user.id,
        'category_id': category.id
    }

    expected_data = {
        'id': 1,
        'name': 'test_ad_name',
        'price': 111,
        'description': None,
        'is_published': False,
        'image': None,
        'author_id': user.id,
        'category_id': category.id
    }

    response = client.post('/ad/', data=data, HTTP_AUTHORIZATION=f"Bearer {access_token}")

    assert response.status_code == 201
    assert response.data == expected_data

