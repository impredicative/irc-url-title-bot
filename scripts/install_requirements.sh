#!/usr/bin/env bash
set -euxo pipefail
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "${DIR}"/..

pip install -U pip wheel
pip install -U -r ./requirements-dev.in
pip install -U -r ./requirements.txt
