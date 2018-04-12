from pyramid.httpexceptions import HTTPNotFound, HTTPFound, HTTPBadRequest
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from ..models import Entry
from . import DB_ERR_MSG
import requests
import os


# https: // pixabay.com/api/docs/
API_KEY = os.environ.get('API_KEY', '')


@view_config(route_name='entries', renderer='../templates/entries.jinja2', request_method='GET')
def entries_view(request):
    try:
        query = request.dbsession.query(Entry)
        user_entries = query.filter(Entry.account_id == request.authenticated_userid)
    except DBAPIError:
        return Response(DB_ERR_MSG, content_type='text/plain', status=500)

    return {'entries': user_entries}


@view_config(route_name='detail', renderer='../templates/detail.jinja2', request_method='GET')
def detail_view(request):
    try:
        entry_id = request.matchdict['id']
    except KeyError:
        return HTTPNotFound()

    try:
        query = request.dbsession.query(Entry)
        entry_detail = query.filter(
            Entry.account_id == request.authenticated_userid).filter(
                Entry.id == entry_id).one_or_none()

    except DBAPIError:
        return Response(DB_ERR_MSG, content_type='text/plain', status=500)

    if entry_detail is None:
        raise HTTPNotFound()

    res = requests.get('https://pixabay.com/api?key={}&q={}'.format(
        API_KEY, entry_detail.title.split(' ')[0]))

    try:
        url = res.json()['hits'][0]['webformatURL']
    except (KeyError, IndexError):
        url = 'https://via.placeholder.com/300x300'

    return {
        "entry": entry_detail,
        "img": url,
    }


@view_config(route_name='new', renderer='../templates/new.jinja2')
def new_view(request):
    if request.method == 'POST':
        if not all([field in request.POST for field in ['title', 'body', 'date', 'author']]):
            raise HTTPBadRequest

        instance = Entry(
            account_id=request.authenticated_userid,
            title=request.POST['title'],
            body=request.POST['body'],
            date=request.POST['date'],
            author=request.POST['author'],
        )

        try:
            request.dbsession.add(instance)
        except DBAPIError:
            return Response(DB_ERR_MSG, content_type='text/plain', status=500)

        return HTTPFound(location=request.route_url('entries'))
    if request.method == 'GET':
        return {}
