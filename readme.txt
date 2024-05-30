# zbleichbyon
# How to build and run
docker build -t myimage .
docker run -p 8080:8080 myimage

# The solution uses MongoDB - db name is hardcoded to zbleichbyon, and tasks are added to a "tasks" collection.

# The solution was written in python with the fastapi framework - the apis are available at http://127.0.0.1:8080/v1/tasks

# Each time you call /v1/tasks with post method a new document will be created in the tasks collection.
# The _id of the created document will be created by the Mongo service, and it will be returned to the user for future use.
# Including a value for "id" in the post request body is possible but meaningless, the user can't choose the document id:
curl -X 'POST' \
  'http://127.0.0.1:8080/v1/tasks' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "1",
  "description": "2",
  "status": "completed",
  "id": "myid"

}'

Response body
{
  "title": "1",
  "description": "2",
  "status": "completed",
  "id": "6658a71ca45ecc1b80ea61db"
}

# An update using the patch method is possible to all task fields EXCEPT for the id (status, title, description).
# An attempt to update other fields will not raise an error, those new values will just be ignored.
curl -X 'POST' \
  'http://127.0.0.1:8080/v1/tasks' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "hello",
  "description": "world",
  "status": "not completed"
}'

{
  "title": "hello",
  "description": "world",
  "status": "not completed",
  "id": "6658a7dc24b07cf22e8b4934"
}

curl -X 'PATCH' \
  'http://127.0.0.1:8080/v1/tasks/6658a7dc24b07cf22e8b4934' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "status": "completed",
  "id": "I WANT A NEW ID",
  "newfield": "AND A NEW FIELD"
}'

{
  "title": "hello",
  "description": "world",
  "status": "completed",
  "id": "6658a7dc24b07cf22e8b4934"
}

# For more information check the fastapi generated docs that are available at http://127.0.0.1:8080/docs
