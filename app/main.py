# create a fastapi app
# the app should respond with 'Hello World' when a GET request is made

import uvicorn
from fastapi import FastAPI
app = FastAPI()


@app.get("/")
def hello_world():
    return "Hello Bastian"

# run the app with uvicorn
# uvicorn app:app --reload
# --reload flag will reload the server when changes are made to the code

# open the app in the browser
# use python api of uvicorn to open the app in the browser


if __name__ == "__main__":
    uvicorn.run("app:app", reload=True, host="0.0.0.0", port=80)
