# Introduction

This project aims to help people understand content in Wikipedia more easily.
This project tries to accomplish this by generating information using AI, with the default model being GPT-3 Davinci from OpenAI, but other models can also be used. The current version generates summaries of sub sections of an article.

For example, in the article [https://en.wikipedia.org/wiki/Calculus](https://en.wikipedia.org/wiki/Calculus), there is a sub section named "Differential calculus". The AI model can be used to generate a summary for a 5-year-old:

_Differential calculus is a way of finding out how something changes. It helps us figure out how fast something is changing, like how fast a car is going or how quickly the temperature is rising. It uses equations and graphs to figure out the rate of change._

Or it can be used to generate a summary for someone who is more familiar with calculus:

_Differential calculus is a branch of calculus that deals with the study of the rates at which quantities change. It is concerned with the study of the properties of functions and their derivatives, which are used to describe the rates of change of the functions. Differential calculus is used to solve problems in many fields, including physics, engineering, economics, and biology._

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

   - Note: Tested with Node 18.7 and npm 9.2.0.

3. Run `npm run dev` to start the client

That's it! The app should now be running on localhost, but there is not a working home page yet, so go to the direct link for an article to get started. For example:

[http://localhost:4000/wiki/Differential_calculus](http://localhost:4000/wiki/Differential_calculus).

[http://localhost:4000/wiki/Michel_Foucault](http://localhost:4000/wiki/Michel_Foucault)

[http://localhost:4000/wiki/University_of_California,\_Davis](http://localhost:4000/wiki/University_of_California,_Davis)
