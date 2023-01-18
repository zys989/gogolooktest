from flask import Flask, request
from pydantic import ValidationError
from task import Task
from redis_om.model import NotFoundError

app = Flask(__name__)


# Utility function to format list of People objects as
# a results dictionary, for easy conversion to JSON in
# API responses.
# def build_results(people):
#     response = []
#     for person in people:
#         response.append(person.dict())
#
#     return {"results": response}


# Create a new person.
@app.route("/task", methods=["POST"])
def create_person():
    try:
        print(request.json)
        new_task = Task(**request.json)
        new_task.save()
        return new_task.pk

    except Exception as e:
        print(e)
        return "It's a bad request!", 400


# # Update a person's age.
# @app.route("/person/<id>/age/<int:new_age>", methods=["POST"])
# def update_age(id, new_age):
#     try:
#         person = Person.get(id)
#
#     except NotFoundError:
#         return "Bad request", 400
#
#     person.age = new_age
#     person.save()
#     return "ok"
#
#
# # Delete a person by ID.
# @app.route("/person/<id>/delete", methods=["POST"])
# def delete_person(id):
#     # Delete returns 1 if the person existed and was
#     # deleted, or 0 if they didn't exist.  For our
#     # purposes, both outcomes can be considered a success.
#     Person.delete(id)
#     return "ok"


# Find a person
@app.route("/tasks", methods=["GET"])
def find_all():
    try:
        # tasks = Task.get()
        for key in Task.pk:
            return Task.get(key)
    except NotFoundError:
        return {}


# Create a RediSearch index for instances of the Person model.
if __name__ == "__main__":
	app.run("127.0.0.1", port="6666", debug=True)