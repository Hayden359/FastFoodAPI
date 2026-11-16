from app import app


def test_home():

    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200


def test_get_all_products():

    client = app.test_client()

    response = client.get(
        "/inventory"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json,
        list
    )


def test_get_product():

    client = app.test_client()

    response = client.get(
        "/inventory/1"
    )

    assert response.status_code == 200


def test_missing_product():

    client = app.test_client()

    response = client.get(
        "/inventory/999"
    )

    assert response.status_code == 404


def test_create_product():

    client = app.test_client()

    response = client.post(
        "/inventory",

        json={
            "name":
            "Pizza",

            "category":
            "Food",

            "price":
            12.99
        }
    )

    assert response.status_code == 201


def test_update_product():

    client = app.test_client()

    response = client.put(
        "/inventory/1",

        json={
            "price":
            7.99
        }
    )

    assert response.status_code == 200


def test_delete_product():

    client = app.test_client()

    response = client.delete(
        "/inventory/2"
    )

    assert response.status_code == 200


def test_search_local_products():

    client = app.test_client()

    response = client.get(
        "/inventory/search/local?name=burger"
    )

    assert response.status_code == 200
    assert response.json[0]["name"] == "Burger"


def test_search_local_products_requires_name():

    client = app.test_client()

    response = client.get(
        "/inventory/search/local"
    )

    assert response.status_code == 400