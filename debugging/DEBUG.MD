# get the list of all the containers which exited
docker ps -a --filter "status=exited" --format "{{.ID}}\t{{.Status}}"

# inspect the contaner id
docker inspect 9784c8d8ba29

# list it by the ID
docker logs 9784c8d8ba297777b89e2cc0e8e70642534b0b4fe4fcd0a4c3b5d5788aa3c20a

# how to ssh into a docker container id
docker exec -it 37725f0c9dcd /bin/bash
----------------------------------------------------------------------------------------
### LOCAL APP DEBUGGING ###
cd /home/ishan/projects/Intelli_OCR/msdocs-python-fastapi-webapp-quickstart_01_26/IntelliReceiptOCR

#virtualenv -p /usr/bin/python3 ocrproj
source ocrproj/bin/activate

gunicorn main3:app -c gunicorn.conf.py
#gunicorn main:app --workers 10 --worker-class uvicorn.workers.UvicornH11Worker --bind 0.0.0.0:8086



# make sure to test the app from the 'docs' not from the HTML application because it's pointing the form submit to somewhere else
-> test it in http://192.168.2.59:3101/docs


sudo dmesg | grep gunicorn

sudo netstat -an | grep 3101

ps aux | grep gunicorn

sudo pkill gunicorn


./startup.sh
--------------------------------------------------------------------------------------------------------
