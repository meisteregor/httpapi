# httpapi

INSTALL
# build egg package
./setup.py bdist_egg
# install dependencies
python3(.6) -m easy_install dist/http_api-1.0-py3.5.egg
# index test data
python3 ./dist/http_api-1.0-py3.5.egg index --db index.db --data ../test_data
# run HTTP service
python3 ./dist/http_api-1.0-py3.5.egg service --db index.db --port 5001
# REST:
take a look into usage screenshots JPG
