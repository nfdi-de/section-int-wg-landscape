#!/usr/bin/env -S uv run --script

# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "pandocfilters>=1.5.1",
# ]
# ///

# adapted from https://github.com/oviquezr/pandoc-mermaid-filter/blob/a663828ea69c9b5716e28ade897a8cae29863155/pandoc_mermaid_filter.py

import os
import subprocess
import sys

from pandocfilters import (
    Image,
    Para,
    get_caption,
    get_extension,
    get_filename4code,
    toJSONFilter,
)

# Environment variables with fallback values
MERMAID_BIN = os.path.expanduser(os.environ.get("MERMAID_BIN", "mmdc"))
PUPPETEER_CFG = os.environ.get("PUPPETEER_CFG", None)


def mermaid(key, value, format_, _):
    if key != "CodeBlock":
        return None

    [[ident, classes, keyvals], code] = value

    if "mermaid" in classes:
        caption, typef, keyvals = _get_caption(keyvals, format_)

        # Use arguments in filename encoding to re-render when flags change
        filename = get_filename4code("mermaid", code + str(keyvals))
        filetype = get_extension(format_, "png", html="svg", latex="png")

        src = filename + ".mmd"
        dest = filename + "." + filetype

        if not os.path.isfile(dest):
            txt = code.encode(sys.getfilesystemencoding())
            with open(src, "wb") as f:
                f.write(txt)

            # Default command to execute
            cmd = [MERMAID_BIN, "-i", src, "-o", dest]

            if PUPPETEER_CFG is not None:
                cmd.extend(["-p", PUPPETEER_CFG])

            if os.path.isfile(".puppeteer.json"):
                cmd.extend(["-p", ".puppeteer.json"])

            if os.path.isfile(".mermaid-config.json"):
                cmd.extend(["-c", ".mermaid-config.json"])

            if os.path.isfile(".mermaid.css"):
                cmd.extend(["-C", ".mermaid.css"])

            for it in keyvals:
                if it[0] == "scale":
                    cmd.extend(["-s", it[1]])

            subprocess.check_call(cmd, stdout=sys.stderr)
            sys.stderr.write("Created image " + dest + "\n")

        return Para([Image([ident, [], keyvals], caption, [dest, typef])])


def _get_caption(item, fmt: str):
    captions, typef, keyvals = get_caption(item)
    # print('Originals: ',captions,typef,keyvals, file=sys.stderr)
    for caption in captions:
        if caption["c"] is None and caption["c"]:
            continue
        caption["t"] = "RawInline"
        caption["c"] = [fmt, to_format(caption["c"], fmt)]
    # print('Captions: ', captions, 'typef: ', typef, 'keyvals: ', keyvals, file=sys.stderr)
    return captions, typef, keyvals


def to_format(txt: str, fmt: str) -> str:
    command = ["pandoc", "-f", "markdown", "-t", fmt]
    p = subprocess.Popen(
        command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    output = p.communicate(input=txt.encode())[0].decode()
    # print("Converted to:", output, file=sys.stderr)
    return output


def main():
    toJSONFilter(mermaid)


if __name__ == "__main__":
    main()
