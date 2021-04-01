import click
from paste.httpserver import serve
from pydap.wsgi.ssf import ServerSideFunctions


@click.command()
@click.option("-h", "--handler-type")
@click.option("-f", "--filename")
@click.option("-p", "--port", default=8001)
def run_handler(handler_type, filename, port):
    module = f"pydap_extras.handlers.{handler_type}"
    _test = getattr(__import__(module, fromlist=["_test"]), "_test")

    handler_name = f"{handler_type.upper()}Handler"
    Handler = getattr(__import__(module, fromlist=[handler_name]), handler_name)

    _test()
    application = Handler(filename)
    application = ServerSideFunctions(application)
    serve(application, port=port)


if __name__ == "__main__":
    run_handler()
