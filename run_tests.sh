export PYTHONPATH=${PWD}:${PWD}/tests:$PYTHONPATH
python -m unittest $1
