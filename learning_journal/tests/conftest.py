import os
import pytest
from pyramid import testing
from ..models.meta import Base
from ..models import Entry


@pytest.fixture
def test_entry():
    return Entry(
        title='fake title',
        body='some fake body of information',
        date='01-01-2018',
        author='Fakey McFaker',
    )


@pytest.fixture
def configuration(request):
    """Setup a database for testing purposes."""
    config = testing.setUp(settings={
        # 'sqlalchecmy.url': 'postgres://localhost:5432/entries_test'
        'sqlalchemy.url': os.environ['TEST_DATABASE_URL']
    })
    config.include('learning_journal.models')
    config.include('learning_journal.routes')

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture
def db_session(configuration, request):
    """Create a database session for interacting with the test database."""
    SessionFactory = configuration.registry['dbsession_factory']
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    """Create a dummy GET request with a dbsession."""
    return testing.DummyRequest(dbsession=db_session)
