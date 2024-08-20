#!/usr/bin/env python

from argparse import ArgumentParser, ArgumentTypeError
from os import chdir
from pathlib import Path
from re import compile
from shutil import which
from subprocess import call
from tempfile import TemporaryDirectory
from typing import NamedTuple

RE_IMPORT = compile(r"^\s*(/\*.*?\*/)?\s*import\s+")


class Args(NamedTuple):
    files: list[Path]


def parse_args() -> Args:
    p = ArgumentParser()
    p.add_argument("files", nargs="+", type=_path)
    return Args(**p.parse_args().__dict__)


def _path(s: str) -> Path:
    x = Path(s)
    if not x.is_file():
        raise ArgumentTypeError(f"{s}: invalid file")
    return x


def main(args: Args) -> int:
    if not which("groovyc"):
        raise RuntimeError("Groovy compiler `groovyc` not found; check PATH")

    with TemporaryDirectory() as tmp:
        input_files = []
        for f in args.files:
            p = f.parents[0]
            (tmp / p).mkdir(parents=True, exist_ok=True)
            tf = tmp / f
            tf.write_text(filter_imports(f))
            input_files.append(tf)
        chdir(tmp)
        return call(["groovyc", "-d", tmp, *input_files])


def filter_imports(p: Path) -> str:
    """Filter out `import org.foo.bar` as local Groovy has no idea of Jenkins modules"""
    with open(p) as f:
        content = f.readlines()
    output = [s for s in content if not RE_IMPORT.match(s)]
    return "".join(output)


def _main() -> None:
    exit(main(parse_args()))


if __name__ == "__main__":
    _main()
