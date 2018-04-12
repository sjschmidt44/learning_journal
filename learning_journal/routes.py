def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('auth', '/auth')
    config.add_route('logout', '/logout')
    config.add_route('entries', '/entries')
    config.add_route('detail', '/detail/{id}')
    config.add_route('new', '/new')
