# HOW TO RUN THE SERVER

Start the server by running the following command from the root directory:

```uvicorn socialmediaapi.main:app --reload```

# USING PYTHON AS AN HTTP CLIENT

The *./requeststest* folder contains a group of scripts that test the endpoints in the project.
 
You can use your own clients to test the end points, using Python, Postman, or any other client out there. 
But you can use these scripts as well in case you're curious about how to use Python as an HTTP client. 

> Example:
>
> Run ```python requeststest/get_all_posts.py``` to see all posts in the database printed in the standard output.

**_These scripts are not part of the project._**