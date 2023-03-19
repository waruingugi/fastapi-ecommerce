# Project
- Name: Ecommerce
- Language: Python 3.10
- Framework: FastAPI
--- 

## Project Details  
This is a FastAPI bare-bones ecommerce app without an ordering feature.
Why not have the ordering feature or other features?
Well, the main aim of the project was to design permissions, filtering, modeling e.t.c
as they are in real world companies.
Any other feature that wasn't within the scope of learning advanced FastAPI implemention was termed as just adding aesthetic value.
And by definition, most of it would have been easy to learn through FastAPI tutorials online.
This project was to learn what you wouldn't find easily online but expected to grasp while in employment.
Hopefully someday I'll create a tutorial for it.

---
## Advanced features
### Authentication/Permissions
- Storing user credentials
- Improving authentication speed using redis
- Restricting CRUD actions based on user type

### Filters and queries
- The method used in querying is a slight improvement of what I found in the company I worked in.
- I created a custom [fastapi filter](https://pypi.org/project/fastapi-sqlalchemy-filter/) package to achieve advanced relationship models filtering.
- This means that I was able to meet the same goals with much less code that was easier to understand.
- The queries also use a DAO structure ensuring uniformity.
----

## Project setup
- Create a virtual environment
- Install packages via poetry
- Create database
- Create and env. file with the varialbes defined in the `Settings` class found in `app/core/config.py`
- In your virtual environment, run ´prestart.sh´ in the terminal.
- And start the server by running ´run.sh´ in the terminal
