# library_rest_api
Book library Rest API that wrote on a Django Rest Framework.
API fetches books from Google endpoint "https://www.googleapis.com/books/v1/volumes" and stores them in database.
Application has next endpoints for fetching data from database:

DOMAINNAME/api/db?q=BookName # fetches books to database

DOMAINNAME/api/books # show book list stored in database

DOMAINNAME/api/books?published_date=2002 # filter by published year

DOMAINNAME/api/books?sort=-published_date # sort by published date

DOMAINNAME/api/books?author=Author Name # filter by author name