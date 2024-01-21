# get the list of all the containers which exited
docker ps -a --filter "status=exited" --format "{{.ID}}\t{{.Status}}"

# inspect the contaner id
docker inspect 9784c8d8ba29

# list it by the ID
docker logs 9784c8d8ba297777b89e2cc0e8e70642534b0b4fe4fcd0a4c3b5d5788aa3c20a

# how to ssh into a docker container id
docker exec -it 37725f0c9dcd /bin/bash

