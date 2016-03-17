## Project Architecture
### Assignment 3
- Based on your analysis, choose an architecture / platform to use for developing your solution (Node, PHP, JSP, etc). Explain why you believe that this particular architecture is the right choice. In addition, write a paragraph that examines an alternate platform and why you believe that it is not the correct choice. 
					
The team has decided to build our application Wagyr on the popular web framework Django, supported on an AWS EC2 Ubuntu instance.  The database will be relational, and we chose MySQL to handle this.  The front end will be supported by the Bootstrap framework and compiled using Django’s templating engine.  Our app will sit behind a Nginx web server and be managed by Gunicorn with several worker threads. 

The architecture that we chose for our project is ideal because it suits the skills of our team members and is appropriate for the scope we have decided on.  Our team has a strong background in python and Django has many modules adept at performing functions like filtering for query strings.  In addition, the ORM is quite capable of using python models to create exactly what we want in MySQL.

The close contender with Django was a MEAN stack.  We did chose this route for several reasons.  Mainly, most of the group was not familiar with JS or MongoDB.  This seemed like a learning curve that was not worth pursuing since the goal of this project is more process based than technology based.  Also, we believed that a NoSQL database was not the right approach to handling an application that’s data needs to be both Consistent and Available (since it involves money and accurate results), and that scalability and Partition tolerance are not particularly important.

Currently, our application is running at http://52.24.228.64/.
