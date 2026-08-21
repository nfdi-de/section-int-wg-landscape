format:
    pnpx prettier --prose-wrap always --write --check "*.md"
    just --fmt
    uv run -m nfdi_kg.lint
    ruff format .
    ruff check --fix .

install-mermaid:
    #!/usr/bin/env bash
    if ! command -v mmdc >/dev/null 2>&1; then
        npm install -g @mermaid-js/mermaid-cli
    else
        echo "mermaid-cli already installed"
    fi

charter:
    just install-mermaid
    pandoc \
      charter/charter.md \
      --filter charter/mermaid_filter.py \
      -o charter/charter.pdf

serve:
    # Note that the 4.2.0 tag is important - 4.2.2 (latest, released ~2022) does not work.
    docker run --rm --volume="$PWD:/srv/jekyll" -p 4000:4000 -it jekyll/jekyll:4.2.0 jekyll serve
