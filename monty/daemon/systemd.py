import os
import sys
from io import StringIO

from loguru import logger
from mako.runtime import Context
from mako.template import Template


def main() -> None:
    logger.info("Creating systemd service...")
    tmpl = Template(filename="monty/daemon/monty.service.mako")
    cwd = os.getcwd()
    buf = StringIO()

    logger.info("Creating output folder...")
    os.makedirs(f"{cwd}{os.path.sep}gen", exist_ok=True)
    logger.info("Rendering file...")
    ctx = Context(buf, monty_root=cwd)

    with open("gen/monty.service", "w") as f:
        tmpl.render_context(ctx)
        logger.info("Writing file...")
        f.write(buf.getvalue())
        logger.info("Done!")
        sys.exit(0)
