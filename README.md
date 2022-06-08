# fast-ledger
a simple ledger system developed with fastapi

### This API assumes the following functionalities and constraints to enforce security and integrity
- users can register on the platform
- users can create up to to ten(10) different accounts.
- Abilities for users to be able to fund and withdraw money to their accounts.
- users can transfer funds to other users and their own accounts.
- users mush have at least 10 ```tokens``` in their accounts


- Find the API documentation [here](https://ledger-app.herokuapp.com/docs)


### Install Pacakges

```
$ pip install -r requirements.txt

```

Then you can then finally start the development server with the command

```
$ uvicorn application:app --reload

```
