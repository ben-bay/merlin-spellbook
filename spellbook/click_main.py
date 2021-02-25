import logging
import os
import sys
import traceback

import click


LOG = logging.getLogger("spellbook")
PLUGIN_DIR = os.path.join(os.path.dirname(__file__), "commands")


class SpellbookCLI(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(PLUGIN_DIR):
            if filename.startswith("__"):
                continue
            if filename.endswith(".py"):
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        ns = {}
        fn = os.path.join(PLUGIN_DIR, name + ".py")
        if not os.path.isfile(fn):
            return
        with open(fn) as f:
            code = compile(f.read(), fn, "exec")
            eval(code, ns, ns)
        return ns["cli"]


def main():
    cli = SpellbookCLI(help="Merlin Spellbook!")  # TODO add --level, --version
    if len(sys.argv) == 1:
        with click.Context(cli) as ctx:
            click.echo(cli.get_help(ctx))
        return 1
    # setup_logging(logger=LOG, log_level="INFO", colors=True)  # TODO level
    try:
        cli()
    except Exception as e:
        #LOG.debug(traceback.format_exc())
        print(traceback.format_exc())
        LOG.error(str(e))
        return 1


if __name__ == "__main__":
    sys.exit(main())
