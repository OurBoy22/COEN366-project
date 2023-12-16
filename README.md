# How to Run Client Server FTP
Download the repo
Create 2 terminals, 1 for client and 1 server
navigate to the project directory, you should see a "server" and "client" directory.

## Start Server
Go into server directory
- cd /server
Start the server first:
- python3 ./server.py
Select udp or tcp connection

## Start Client
Go into client directory
Start the Client (Keep in mind that the IP. port # can be modified at the beggining of the server.py file)
- python3 ./client.py
- Enter the server name: 127.0.0.1
- Enter the port number: 12000
- Enter the connection type: TCP or UDP

Client will be connected to server
## Client Commands
In the client terminal, write:
#### put
- put "filename.txt" (can be any other extension type)

Server will receive the filename.txt

#### get
- get "filename.txt"

Client will receive the filename.txt

#### summary
- summary numbers.txt

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

