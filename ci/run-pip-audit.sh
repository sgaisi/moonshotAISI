#!/bin/bash

# install dependencies
source .venv/bin/activate
uv sync --all-packages --inexact > /dev/null

# license check
echo "License check..."
uv pip install pip-licenses > /dev/null
uv run pip-licenses --format markdown --output-file licenses-found.md > /dev/null
uv pip uninstall pip-licenses prettytable wcwidth > /dev/null

# dependency check
echo "Dependency check..."
uv pip install pip-audit > /dev/null
uv pip uninstall setuptools > /dev/null
set +e
uv run pip-audit --format markdown --desc on -o pip-audit-report.md &> pip-audit-count.txt
exit_code=$?
uv pip install mdtree > /dev/null

if [ -f pip-audit-report.md ]; then
  echo "============ Vulnerabilities Found ============"
  cat pip-audit-report.md
  mdtree pip-audit-report.md > pip-audit-report.html
else
  touch pip-audit-report.html
fi

if [ -f licenses-found.md ]; then
  strongCopyleftLic=("GPL" "AGPL" "EUPL" "OSL")
  weakCopyleftLic=("LGPL" "MPL" "CCDL" "EPL" "CC-BY-SA" "CPL")

  echo "============ Strong Copyleft Licenses Found ============"
  head -n 2 licenses-found.md
  while IFS= read -r line; do
    # Skip text-unidecode with Artistic Licenses
    if [[ $line == *"text-unidecode"* ]] && [[ $line == *"Artistic License"* ]]; then
      continue
    fi
    for lic in "${strongCopyleftLic[@]}"; do
      if [[ $line == *"$lic"* ]]; then
        echo "$line"
        break
      fi
    done
  done < licenses-found.md

  echo "============ Weak Copyleft Licenses Found ============"
  head -n 2 licenses-found.md
  while IFS= read -r line; do
    # Special case for text-unidecode
    if [[ $line == *"text-unidecode"* ]] && [[ $line == *"Artistic License"* ]]; then
      echo "$line (Reclassified as weak copyleft)"
      continue
    fi
    for lic in "${weakCopyleftLic[@]}"; do
      if [[ $line == *"$lic"* ]]; then
        echo "$line"
        break
      fi
    done
  done < licenses-found.md
  mdtree licenses-found.md > license-report.html
else
  touch license-report.html
fi

deactivate
rm -rf ci-venv

set -e
if [ $exit_code -ne 0 ]; then
#  echo "pip-audit failed, exiting..."
  exit $exit_code
fi
