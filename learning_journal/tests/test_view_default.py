# Default view properties


def test_default_response_home_view(dummy_request):
    from ..views.default import home_view

    response = home_view(dummy_request)
    assert len(response) == 0
    assert type(response) == dict


# Auth View Functionality
def test_default_response_auth_view(dummy_request):
    from ..views.default import auth_view

    response = auth_view(dummy_request)
    assert response.status_code == 200


def test_auth_signin_view(dummy_request):
    from ..views.default import auth_view
    from pyramid.httpexceptions import HTTPFound

    dummy_request.GET = {'username': 'watman', 'password': 'whodat'}
    response = auth_view(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)


def test_auth_signup_view(dummy_request):
    from ..views.default import auth_view
    from pyramid.httpexceptions import HTTPFound

    dummy_request.POST = {'username': 'watman', 'password': 'whodat', 'email': 'wat@wat.com'}
    dummy_request.method = 'POST'
    response = auth_view(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)


def test_bad_reqeust_auth_signup_view(dummy_request):
    from ..views.default import auth_view
    from pyramid.httpexceptions import HTTPBadRequest

    dummy_request.POST = {'password': 'whodat', 'email': 'wat@wat.com'}
    dummy_request.method = 'POST'
    response = auth_view(dummy_request)
    assert response.status_code == 400
    assert isinstance(response, HTTPBadRequest)


def test_bad_request_method_auth_signup_view(dummy_request):
    from ..views.default import auth_view
    from pyramid.httpexceptions import HTTPFound

    dummy_request.POST = {'password': 'whodat', 'email': 'wat@wat.com'}
    dummy_request.method = 'PUT'
    response = auth_view(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)

