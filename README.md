<h1 align="center">Django Blog</h1>

## I. General info

My django project hosted on heroku. Database was created via Amazon RDS (Relational Database Service) with PostgreSQL engine.

## II. Used technologies 
* Django 4.0.1
* Python 3.9.10
* Bootstrap
* PostgreSQL
* Amazon RDS - Relational Database Service
* Amazon S3 - Cloud Object Storage
* Heroku - Cloud Application Platform

## III. Installation
1. Download this repository.
    ```
   git clone https://github.com/kzaleskaa/django-blog.git
   cd first-django-blog
   ```
2. Create your own Python virtual environment.
    ```
   python -m venv venv
   ```
3. Activate created environment.
    ```
    venv/Scripts/activate
    ```
4. Install all necessary packages.
    ```
    pip install requirements.txt
    ```
5. Add environment variables: 
    ```
    SECRET_KEY=<DJANGO SECRET KEY>

    # email 
    EMAIL_HOST_USER=<EMAIL ADDRESS>
    EMAIL_HOST_PASSWORD=<PASSWORD OF EMAIL ADDRESS>

    # database 
    DATABASES_PASSWORD=<DATABASE PASSWORD>  
    DATABASES_HOST=<ENDPOINT>
    DATABASES_USER=<MASTER USERNAME>

    # AWS
    AWS_ACCESS_KEY_ID=<AWS ACCESS KEY ID>
    AWS_SECRET_ACCESS_KEY=<AWS SECRET ACCESS KEY>
    AWS_STORAGE_BUCKET_NAME=<AWS STORAGE BUCKET NAME>
    ```
6. Set DEBUG=True 
7. Create superuser to get access to administration site.
    ```
    python manage.py createsuperuser
    ```
8. Run app.
    ```
    python manage.py runserver
    ```
## IV. Sessions
We can keep track of the "state" between the site and a particular browser. Every item associated with the session has a "key", which is used to store and retrieve data. In this app user can save post to read it later or remove item from saved posts.
```python
# save post_id from post request
post_id = int(request.POST["post_id"])

# add or remove post based on current state of session
if post_id not in stored_posts:
    stored_posts.append(post_id)
else:
    stored_posts.remove(post_id)

# save created item
request.session["stored_posts"] = stored_posts
```

## V. Registration and authentication
You can't add your own posts or comments without logging in. To get access to these functions you should create your own account. When you fill out the registration form correctly, you'll receive welcome and confirmation mail from django.first.project@gmail.com. 

## VI. Final effect
<p align="center" width="100%">
    <img width="30%" src="https://user-images.githubusercontent.com/62251989/154593885-eb817f34-4843-4e27-a4a6-ca1d17536770.png">
    <img width="30%" src="https://user-images.githubusercontent.com/62251989/154594268-dd207f83-cd44-4c38-b1c4-0800f18b92f3.png">
    <img width="30%" src="https://user-images.githubusercontent.com/62251989/154593765-3b73bbdb-c715-4c73-a58d-dba8f2dfecbd.png">    
</p> 

<div align="center">
<img width="90%" src="https://user-images.githubusercontent.com/62251989/154593062-d827e973-c538-4092-8e38-cc70b894b046.png">
</div>
