httpapi

BUILD EGG
./setup.py bdist_egg

INSTALL
python3.(5) -m easy_install http_api-1.0-py3.5.egg

INDEX DATA
python3 ./dist/http_api-1.0-py3.5.egg index --db index.db --data your_data

RUN HTTP SERVICE
python3 ./dist/http_api-1.0-py3.5.egg service --db index.db --port 5001

USE
http://hostname:port//<keyword..>//?search=&param= 
default search by values with intersection 
(...?search=&param=) search=key - by keys param=d - disjunction