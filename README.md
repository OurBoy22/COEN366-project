# How to Run Client Server FTP
Download the repo
Create 2 terminals, 1 for client and 1 server

## Start Server
Go into server directory
Start the server first:
- python3 ./server.py

## Start Client
Go into client directory
Start the Client
- python3 ./client.py
- Enter the server name: 127.0.0.1
- Enter the port number: 12000
- Enter the connection type: TCP or UDP

Client will be connected to server
## Client Commands
In the client terminal, write:
#### put
- put "filename.txt" 

Server will receive the filename.txt

#### get
- get "filename.txt"

Client will receive the filename.txt

#### summary
- summary numbers

Client will get a summary of the file

#### change
- change "oldname.txt" "newname.txt"

"oldname.txt" file will be rename to "newname.txt" 

#### help
- help

Console will display the commands

#### bye
- bye

Client will disconnect to server and will be terminated

