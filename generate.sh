#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR=$(dirname "$(realpath $0)")
PY_SRC="${SCRIPT_DIR}/src/bdkpython/"

echo "Generating bdk.py..."
BDKFFI_BINDGEN_OUTPUT_DIR="$PY_SRC" BDKFFI_BINDGEN_PYTHON_FIXUP_PATH=bdkffi cargo run --manifest-path ./bdk-ffi/Cargo.toml --package bdk-ffi-bindgen -- --language python --udl-file ./bdk-ffi/src/bdk.udl --release
