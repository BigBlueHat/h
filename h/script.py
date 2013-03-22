import clik

from pyramid.scripts import pserve

from h import __version__


version = __version__
description = """\
The Hypothes.is Project Annotation System
"""


command = clik.App(
    'hypothesis',
    version=version,
    description=description,
)


@command(usage='CONFIG_FILE')
def assets(args, console):
    """Build the static assets."""

    if len(args) == 0:
        console.error('You must supply a paste configuration file.')
        return 2

    from h import bootstrap
    from pyramid_webassets import IWebAssetsEnvironment

    def build(env):
        asset_env = env['registry'].queryUtility(IWebAssetsEnvironment)
        for bundle in asset_env:
            bundle.urls()

    bootstrap(args[0], config_fn=build)


@command
def start(args):
    """Start the server.

    With no arguments, starts the server in development mode using the
    configuration found in `deveopment.ini` and a hot code reloader enabled.
    """
    if not len(args):  # Default to dev mode
        pserve.ensure_port_cleanup([('0.0.0.0', 5000)])
        args.append('development.ini')
        args.append('--reload')

    pserve.main(['hypothesis'] + args)


main = command.main
