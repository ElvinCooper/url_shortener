from urlshort import create_app

def test_shorten(cliente):
    response = cliente.get('/')
    assert b'Shorten' in response.data
