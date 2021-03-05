#!/usr/bin/env bash
function killall() {
    echo "Killing:"
    jobs
    jobs -p | xargs kill
}

trap killall SIGINT

.venv/bin/python -u app.py 1 5050 &
.venv/bin/python -u app.py &
wait
