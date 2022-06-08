# fast-ledger
a simple ledger system developed with fastapi

### This API assumes the following functionalities and constraints
- users can register on the platform
- users can create up to to ```ten(10)``` different accounts.
- Abilities for users to be able to fund and withdraw money to their accounts.
- users can transfer funds to other users and to their own accounts.
- users mush have at least 10 ```tokens``` in their accounts

### Getting Started 
To get started with the project, ensure you have setup and activated a virtual environment, guides on that [here](https://realpython.com/python-virtual-environments-a-primer/)

clone the repository via the command

```
$ git clone https://github.com/E-wave112/fast-ledger.git
```

### Install Pacakges
navigate to the directory of your virtual environment and install all the required dependencies there

```
$ pip install -r requirements.txt

```

Then you can then finally start the development server with the command

```
$ uvicorn application:app --reload

```
- The api will be running on host [localhost:8000](http://localhost:8000)
