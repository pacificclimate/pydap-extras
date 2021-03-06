import click
from paste.httpserver import serve
from pydap.wsgi.ssf import ServerSideFunctions


@click.command()
@click.option(
    "-h",
    "--handler-type",
    help="Convert between the handler-type format and the data model used by Pydap",
    type=click.Choice(["sql", "csv", "pcicsql", "rawpcicsql", "climopcicsql"]),
)
@click.option(
    "-a",
    "--args",
    default=(None),
    multiple=True,
    help="Arguments to initiate the handler",
)
@click.option("-p", "--port", default=8001)
def run_handler(handler_type, args, port):
    handler_names = {
        "sql": "SQL",
        "csv": "CSV",
        "pcicsql": "PcicSql",
        "rawpcicsql": "RawPcicSql",
        "climopcicsql": "ClimoPcicSql",
    }

    if "pcic" in handler_type:
        module = f"pydap_extras.handlers.pcic"
    else:
        module = f"pydap_extras.handlers.{handler_type}"
        _test = getattr(__import__(module, fromlist=["_test"]), "_test")
        _test()

    handler_name = f"{handler_names[handler_type]}Handler"
    Handler = getattr(__import__(module, fromlist=[handler_name]), handler_name)

    application = Handler(*args)
    application = ServerSideFunctions(application)
    serve(application, port=port)


if __name__ == "__main__":
    run_handler()
