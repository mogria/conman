#!/bin/sh
PYTHON=""
find_python3() {
    echo -n "Searching for python3 ..."
    for search in "python" "python3" "/usr/bin/env python" "/usr/bin/env python3"; do
        echo ""
        echo -n "testing $search ... "
        output="$("$search" -c 'import sys; print(sys.version_info[0])')"
        if [ "$?" -eq 0 ]; then
            if [ "$output" -eq 3 ]; then
                PYTHON="$search"
                echo "ok"
                break
            else
                echo -n "not version 3"
            fi
        else
            echo -n "invalid executable"
        fi
    done
}

if [ ! -d '/tmp/conman-build' ]; then
    echo "Fetching repostory"
    git clone "https://github.com/mogria/conman.git" /tmp/conman-build
else
    echo "Updating repository"
    (cd '/tmp/conman-build'; git pull)
fi

if [ "$?" -ne 0 ]; then
    echo "couldn't fetch git repository. Aborting"
    exit 1
fi

find_python3
if [ -z "$PYTHON" ]; then
    echo "no python 3 found"
    exit 2
fi

cd /tmp/conman-build
echo "Building ..."
"$PYTHON" setup.py build
if [ "$?" -ne 0 ]; then
    echo "build unsuccessful."
    exit 3
fi

echo "Installing (requires sudo) ..."
sudo "$PYTHON" setup.py install
echo "Sucessfully installed conman"

