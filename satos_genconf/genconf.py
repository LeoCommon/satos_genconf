# This file is heavily based on https://gist.github.com/mmerickel/6e484657f2244fc6876e6bfb8ed97bc3
from dotenv import load_dotenv
import jinja2
from jinja2.ext import Extension
from jinja2.lexer import Token
from markupsafe import Markup
import os

# Custom helpers for sato
from .helpers import DeviceInfo

def ini_filter(value):
    if isinstance(value, Markup):
        return value
    if not isinstance(value, str):
        return value
    return value.replace('%', '%%')

class IniEverythingExtension(Extension):
    """
    Insert a `|ini` filter at the end of every variable substitution.
    This will ensure that all injected values are converted to INI.
    """
    def filter_stream(self, stream):
        # This is based on
        # https://github.com/indico/indico/blob/master/indico/web/flask/templating.py.
        for token in stream:
            if token.type == 'variable_end':
                yield Token(token.lineno, 'pipe', '|')
                yield Token(token.lineno, 'name', 'ini')
            yield token

def render_template(path, context):
    base, name = os.path.split(path)
    if not base:
        base = os.getcwd()

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader([base]),
        undefined=jinja2.StrictUndefined,
        extensions=[IniEverythingExtension],
    )
    env.filters['ini'] = ini_filter

    template = env.get_template(name)
    return template.render(context)
    

# This returns the device info dictionary
def getDeviceInfo(args): 
    dev = DeviceInfo(args.mock_run)
    return {
        'model': dev.model(),
        'serialnumber': dev.serialnumber(), 
        'hw_revision': dev.hw_revision(), 
    }

# Opener for files with 0660 permissions
def configOpener(path, flags):
    return os.open(path, flags, 0o660)

def run(args):
    # Reset umask to 0
    os.umask(0)

    # Load the secrets/environment from file if specified
    if args.env_file:
        load_dotenv(args.env_file, override=True)

    result = render_template(args.template, {
        'env': os.environ,
        'device': getDeviceInfo(args),
        'CONFIG_VERSION': 1
    })

    # Write the output config file. See configOpener for more details
    with open(args.output_file, 'w', encoding='utf8', opener=configOpener) as fp:
        fp.write(result.rstrip() + '\n')
