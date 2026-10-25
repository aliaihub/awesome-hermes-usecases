#!/usr/bin/env bash
set -euo pipefail
STARTER_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$STARTER_DIR/../_shared/starter.py" daily-briefing setup --deliver local "$@"
