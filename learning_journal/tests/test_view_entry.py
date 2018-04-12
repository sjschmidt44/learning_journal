# Default view properties


def test_default_response_entries_view(dummy_request):
    from ..views.entry import entries_view

    response = entries_view(dummy_request)
    assert isinstance(response, dict)
    assert response['entries'] == []


def test_default_detail_view(dummy_request, db_session, test_entry):
    from ..views.entry import detail_view

    db_session.add(test_entry)

    dummy_request.matchdict = {'id': '1'}
    response = detail_view(dummy_request)
    assert response['entry'].id == 1
    assert type(response['img']) == str


def test_detail_not_found(dummy_request):
    from ..views.entry import detail_view
    from pyramid.httpexceptions import HTTPNotFound

    response = detail_view(dummy_request)
    assert isinstance(response, HTTPNotFound)


def test_default_response_new_view(dummy_request):
    from ..views.entry import new_view

    response = new_view(dummy_request)
    assert len(response) == 0
    assert type(response) == dict


def test_valid_post_to_new_view(dummy_request):
    from ..views.entry import new_view
    from pyramid.httpexceptions import HTTPFound

    dummy_request.method = 'POST'
    dummy_request.POST = {
        'title': 'fake title',
        'body': 'some fake body of information',
        'date': '01-01-2018',
        'author': 'Fakey McFaker',
    }

    response = new_view(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)


def test_valid_post_to_new_view_adds_record_to_db(dummy_request, db_session):
    from ..views.entry import new_view
    from ..models import Entry

    dummy_request.method = 'POST'
    dummy_request.POST = {
        'title': 'fake title',
        'body': 'some fake body of information',
        'date': '01-01-2018',
        'author': 'Fakey McFaker',
    }

    # assert right here that there's nothing in the DB

    new_view(dummy_request)
    query = db_session.query(Entry)
    one = query.first()
    assert one.title == 'fake title'
    assert one.body == 'some fake body of information'
    assert type(one.id) == int


def test_invalid_post_to_new_view(dummy_request):
    import pytest
    from ..views.entry import new_view
    from pyramid.httpexceptions import HTTPBadRequest

    dummy_request.method = 'POST'
    dummy_request.POST = {}

    with pytest.raises(HTTPBadRequest):
        response = new_view(dummy_request)
        assert isinstance(response, HTTPBadRequest)

