#!/usr/bin/env bash
# Setup di PyRef per l'ambiente locale.
# ./setup_pyref.sh [cartella_destinazione]
# Default cartella destinazione: ./PyRef

set -e

DEST="${1:-PyRef}"

PYVER=$(python3 -c "import sys; print(f'{sys.version_info[0]}.{sys.version_info[1]}')" 2>&1)
if [ "$PYVER" != "3.8" ] && [ "$PYVER" != "3.9" ]; then
    echo "Required Python 3.8 o 3.9 (rilevato: $PYVER)."
    echo "pandas 1.2.2 (required by PyRef) does not have wheel precompilate for Python 3.10+."
    exit 1
fi
echo "Python $PYVER detected, ok."

if [ -d "$DEST" ]; then
    echo "directory $DEST already exist', i am skipping the clone"
else
    echo "Clone PyRef in $DEST ..."
    git clone https://github.com/PyRef/PyRef.git "$DEST"
fi

echo "Dependency installation (from requirements.txt)..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# numpy va reinstallato insieme a pandas per evitare il classico errore di
# incompatibilita' binaria (ValueError: numpy.dtype size changed...) che si
# presenta se un numpy troppo recente resta gia' installato/in cache.
pip uninstall numpy pandas -y >/dev/null 2>&1 || true
pip install -r "$SCRIPT_DIR/requirements.txt"

echo ""
echo "Setup completed. Quick check using (DummyRef)..."
cd "$DEST"
if [ ! -d "Repos/DummyRef" ]; then
    python3 main.py repoClone -u "PyRef" -r "DummyRef"
fi
python3 main.py getrefs -r "Repos/DummyRef" | tail -5
echo ""
echo "If you see an output from the previous command, it means Pyref is ready to work"