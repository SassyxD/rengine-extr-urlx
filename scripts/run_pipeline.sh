#!/usr/bin/env bash
set -euo pipefail
OUT=${1:-data}
DOMAINS=${2:-domains.txt}
make run OUT="$OUT" DOMAINS="$DOMAINS"
