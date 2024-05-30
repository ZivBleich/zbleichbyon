# zbleichbyon
# How to build and run
docker build -t myimage .
docker run -p 8080:8080 myimage

# fastapi generated docs are then available at http://127.0.0.1:8080/docs
# A sanity test can be done with any browser and the address http://127.0.0.1:8080/v1/tasks/ping
