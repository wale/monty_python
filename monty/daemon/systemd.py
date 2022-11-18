import grp
import os
import pwd
import shutil
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

    logger.info("Finding poetry...")
    poetry_path = shutil.which("poetry")

    logger.info("Getting owner and group of folder.")
    stat_info = os.stat(cwd)
    uid = stat_info.st_uid
    gid = stat_info.st_gid

    user = pwd.getpwuid(uid)[0]
    group = grp.getgrgid(gid)[0]

    logger.info("Creating output folder...")
    os.makedirs(f"{cwd}{os.path.sep}gen", exist_ok=True)
    logger.info("Rendering file...")
    ctx = Context(buf, monty_root=cwd, poetry_path=poetry_path, owner=user, group=group)

    with open("gen/monty.service", "w") as f:
        tmpl.render_context(ctx)
        logger.info("Writing file...")
        f.write(buf.getvalue())
        logger.info("Done!")
        sys.exit(0)
