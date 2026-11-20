#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
: "${RELEASE_BASENAME:?RELEASE_BASENAME is required}"
make -C "$ROOT_DIR" release RELEASE_BASENAME="$RELEASE_BASENAME"
