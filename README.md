# BeautifulBlockChain

The goal of this project is to create a little BlockChain.
Done in Security course at HE-Arc school.

## Program commands

Welcome in the BeautifulBlockChain help part.

------ How To Use ------

To use one of this command call this python script following with one of this command, example :
py sources/BBCMain.py -h

*** WARNING *** Don't forget to initialize the blockchain by doing :
py sources/BBCMain.py -i

------ Commands ------

-h : display this page
-i : initialize the base structure of the block chain (create usefull folders and files)
-u : create a new user
-t : make a transaction between 2 user and add it to the blockchain when enough transactions were done
-v : verify the transaction given in parameter (put the transaction between quotation marks)
-d : display the blockchain

--force : used in some command to force an action

## Usefull commands

### Virtual env
Execute this the first time you clone the project.
`python -m venv env --clear`

### Activate virtual env
`source env/Scripts/activate`

### Desactivate virtual env
`deactivate`

### Update pip and install dependencies
`python -m pip install --upgrade pip`  
`python -m pip install -r requirements.txt`
