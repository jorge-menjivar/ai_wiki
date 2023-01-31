# Getting Started

## Prerequisites

1. Install and Run PostgreSQL

2. Create a Python virtual environment.

   - Note: Tested with Python 3.11. You may need to install async libraries manually if using older versions of python.

3. Install the dependencies from `/server/requirements.txt`

```sh
pip install -r ./server/requirements.txt
```

4. Create a `.env` file inside `/server`. Look at `sample.env`, it has all the required variable names.

   - Place your OpenAI key there. You can get one from here: [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
   - Place your PostgreSQL authentication information there.
     - Note: Use `127.0.0.1` instead of `localhost` to prevent auth issues, if running PostgreSQL locally.

5. Start the server. Inside `/server`, run

```
python -m main
```

## Running the app

1. Change to the `/client/` directory

2. Run `npm install` to install the required packages

3. Run `npm run dev` to start the client

That's it! The app should now be running on localhost, but there is not a working home page yet, so go to the direct link for an article to get started. For example:

[http://localhost:4000/wiki/Differential_calculus](http://localhost:4000/wiki/Differential_calculus).

[http://localhost:4000/wiki/Michel_Foucault](http://localhost:4000/wiki/Michel_Foucault)

[http://localhost:4000/wiki/University_of_California,\_Davis](http://localhost:4000/wiki/University_of_California,_Davis)
