# Book Reviewer Backend Application
The backend of the Book Reviewer project uses django (python) and MySQL
## Getting started locally

### Docker Setup
Run below command to build containers of the app.

```bash
- docker-compose up --build
```

### Local Setup
Execute the bash script : runserver.sh

```bash
- bash runserver.sh
```

## Connecting to the Application
You can connect to the application by the default user.

```bash
username : morotech
password : pass 
```
### Backend main URL:

Backend application in your browser at: [http://localhost:8000/](http://localhost:8000/).

### Endpoint examples:

```bash
# Part 1  Get all Gutendex books or Searching functionallity with searching param.
- external/  or  external/?serach=example
# Part 1  Searching functionallity from url kwargs                             
- external/<str:search>/
# Part 1  + Pagination                       
- external/<int:page>/
# Part 2                         
- review/<int:book_id>/
# Part 3                                                
- book/<int:book_id>/   
# Bonus average service, getting the average scores by book_id and year.                                 
- average_month/<int:book_id>/  or  /<int:book_id>/<int:year>/                
# Bonus top books service, getting the top rated N books sorted by top_num from url.                                             
- top_books/<int:top_num>/  
```

### Admin panel URL:
Admin panel in your browser at: [http://localhost:8000/admin/](http://localhost:8000/admin/).


## Database Credentials

```bash
schema   : database
username : morotech
password : pass 
host     : localhost
port     : 3306

```



