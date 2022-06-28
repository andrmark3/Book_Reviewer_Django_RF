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
- api/book/external/Great           # // Part 1 // Searching functionallity from url kwargs.
- api/book/external/?search=Great   # // Part 1 // Searching functionallity from searching param.
- api/book/external/2               # // Part 1 // Pagination
- api/book/review/11                # // Part 2 //                                 
- api/book/book/15                  # // Part 3 //   
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



