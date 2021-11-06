### Built With

This API has been created with.

* [FastAPI](https://fastapi.tiangolo.com/)
* [TortoiseORM](https://tortoise-orm.readthedocs.io/en/latest/)
* [PostgreSQL](https://www.postgresql.org/)




<!-- GETTING STARTED -->
## Getting Started

### Prerequisites
You need to have Python 3.6+ installed
* [Python3](https://www.python.org/downloads/)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/luisregardiz/fastapi
   ```
2. Create a virtual environment with venv (You can use any other)
   ```sh
   python -m venv env
   ```
3. Install packages 
   ```sh
   pip install -r requirements.txt 
   ```

4. Create a .env file and enter the required data 
   ```sh
    #Jwt config
    SECRET_KEY=XXXXXX
    ALGORITHM=XXXXX
    ACCESS_TOKEN_EXPIRE_MINUTES=XX

    #Postgresql
    USER=XXXX
    PASSWORD=XXXXXXXXX
    HOST=XXXXXXX
    PORT=XXXXXX
    DB_NAME=XXXXXXXXX


    #cors 
    CLIENT_URL=http://XXXXXX
   ```
  
5. Run server 
   ```sh
   uvicorn main:app --reload 
   ```



<!-- USAGE EXAMPLES -->
## Usage

To know more information about the API, go to http://localhost:8000/docs



