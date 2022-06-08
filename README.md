# **Movies: Microservice Architecture Project**

#### *Software architecture UCU course 2022*

**Authors:**
- **[Yana Muliarska](https://github.com/muliarska)**
- **[Khrystyna Kokolus](https://github.com/khristinakokolus)**
- **[Yaroslav Prytula](https://github.com/SlavkoPrytula)**


----

<img width="782" alt="image" src="https://user-images.githubusercontent.com/25413268/172652721-823c5ca9-60d1-4593-8c6b-871f3be2fa1d.png">

----

## **Requirement**


Before starting to work with current repository please make sure to download it locally on your machine

### Installation
```bash
git clone https://github.com/muliarska/movies-system/
git fetch
cd movies-system
```

### Folders structure

```
.
├── users-service
│   ├── db_part
│   │   ├── run-postgres.sh
│   ├── app.py
│   └── ...  
├── movies-service
│   ├── db_part
│   │   ├── run-cassandra.sh
│   ├── app.py
│   └── ...  
├── requests_users.http
├── requests_movies.http
└── ...
```

### Docker Build

```bash
bash ./users-service/db_part/run-postgres.sh
bash ./users-service/run-service.sh
```

```bash
bash ./movies_service/db_part/run-cassandra.sh
bash ./movies_service/run-service.sh
```

The application is now running on `5001, 5002` ports

----

## **Idea**

This application introduces the concept of a clean distributed movie system

The platform is built upon **Flask** web framework to define the routes. 
Besides, to improve user experience and app integration the system uses two 
**PostgreSQL** and **Casandra** based databases 
to store all the needed information about the new users and user specific movies

The movie interaction system is build upon introducing the identity mapping. 
- Every single user is isolated in its own space and can control only its content   

<br />


<img width="846" alt="image" src="https://user-images.githubusercontent.com/25413268/172674486-7e4a0176-8f12-4c09-9d0c-5ec7a7e2b3bd.png">



In this project, you will find different types of microservices:
- `user_service`
- `movies_service`

----

## **Usage**

Every service is wrapped as an API, thus user can interact with it using both predefined `.http` files

- `requests_users.http`
- `requests_movies.http`

In the main folder directory files `requests.http` store the needed request commands `(POST/GET)`
You can also use PyCharm IDE, Postman tool, curl, web Dev, etc. to execute the following commands

---

### User Requests 

#### sign_up

```http request
POST http://localhost:5001/movies_api/sign_up
Content-Type: application/json

{
  "username": "johndoe",
  "email": "johndoe@gmail.com",
  "password": "Password12@",
  "name":"John Doe",
  "dob": "01-02-2002"
}
```

#### sign_in

```http request
POST http://localhost:5001/movies_api/sign_in
Content-Type: application/json

{
  "username": "johndoe",
  "password": "Password13@"
}
```


#### profile/[username]

```http request
GET http://localhost:5001/movies_api/profile/johndoe
Content-Type: application/json
```


#### change_password/[username]

```http request
PUT http://localhost:5001/movies_api/change_password/johndoe
Content-Type: application/json

{
  "old_password": "Password12@",
  "new_password": "Password13@"
}
```



#### update_profile/[username]

```http request
PUT http://localhost:5001/movies_api/update_profile/johndoe
Content-Type: application/json

{
  "name": "Jay"
}
```


#### delete_account/[username]

```http request
DELETE http://localhost:5001/movies_api/delete_account/johndoe
Content-Type: application/json

{
  "password": "Password12@"
}
```



<br />

---

### Movies Requests 

#### movies/[user]

```http request
GET http://localhost:5002/movies_api/movies/johndoe
Content-Type: application/json
```

#### trending_movies/[user]

```http request
GET http://localhost:5002/movies_api/trending_now/johndoe
Content-Type: application/json
```


#### add_movie/[movie_name]/[user]

```http request
POST http://localhost:5002/movies_api/add_movie/johndoe
Content-Type: application/json

{
  "title": "hey2",
  "movie_type": "comedy",
  "ratings": 97,
  "duration": 100,
  "age_restriction": 18,
  "description": "great film",
  "cast": "DiCaprio, Joli",
  "genres": "comedy",
  "category": "comedy",
  "production": "great entertainment",
  "country": "UA",
  "is_favourite": "False"
}
```


#### add_to_favourites/[movie_name]/[user]

```http request
PUT http://localhost:5002/movies_api/add_to_favourites/hey5/johndoe
Content-Type: application/json
```


#### favourite_movies/[user]

```http request
GET http://localhost:5002/movies_api/favourite_movies/johndoe
Content-Type: application/json
```


#### search_movie/[movie_name]/[user]

```http request
GET http://localhost:5002/movies_api/search_movie/hey5/johndoe
Content-Type: application/json
```


#### movies_api/[movie_name]/[user]

```http request
DELETE http://localhost:5002/movies_api/delete_movie/hey5/johndoex`
Content-Type: application/json
```

----

## **References**
- [Video Tutorials]('https://www.youtube.com/playlist?list=PLj3AfeFCdPVz9NdfYZztkxwqOZTbLwaEF')
- https://www.psycopg.org/docs/
- https://towardsdatascience.com/python-and-apache-cassandra-for-beginners-d9682f2f43c1
- https://towardsdatascience.com/getting-started-with-apache-cassandra-and-python-81e00ccf17c9
