#!/usr/bin/env bash
# Launch LinguaRead - keeps the repo root clean
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python "$DIR/backend/main.py" "$@"
