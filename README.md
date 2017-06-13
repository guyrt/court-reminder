## court-reminder - what it does
Calling things and transcribing.  

Here we have instructions for running the program on a local machine and on an Azure VM.

# Running on local machine 
## Clone the court reminder repository
git clone <court reminder>

## install python 3   
sudo apt-get update
sudo apt-get install python-dev build-essential libssl-dev libffi-dev python-pip3 -y

## install modules that are needed
sudo pip3 install -r requirements.txt
sudo apt-get install sox -y

## Fill in secrets files (these contain API keys, lists of numbers for which you want info):
The secrets files are located in the following folders:
  1. Storage
  2. Server
  3. Transcription
  4. Call
 You want to copy secrets sample and then fill in the blanks.  You will need to set up your own API keys.

## Run
Two parts:
1. Running the runners (transcribing, calling, extracting)
  - python ./court-reminder/runners.py
2. Running the servers (twiml server, admin server)
  - python start_server.py --twilio_prod
  - python start_server.py --admin_prod

# Running on Azure VM 

## set up azure account
Make an account with Microsoft azure.

## Create virtual machine
Go to portal.azure.com
Go to virtual machine tab
Add Ubuntu server 16.04 LTS (or a recent version that is not LTS because it will have python 3)
Click create
Specify username, and say you want to use password
PS1_V2 is a good plan
Keep settings as is
In overview, you can get your public IP.

## Allow http access
Go to network interfaces
Retrieve name of security group
Search for name of security roup
Add new rule to inbound security rules 
Port range 8080. Name httpaccess
Password for this will be in the secrets.py file in the server folder in the repo

## ssh into the azure account
ssh <username>@<IP address>

## Clone the court reminder repository
git clone <court reminder repo>

## install python 3   
sudo apt-get update
sudo apt-get install python-dev build-essential libssl-dev libffi-dev python-pip3 -y

## install modules that are needed
sudo pip3 install -r requirements.txt
sudo apt-get install sox -y

## Fill in secrets files (these contain API keys, lists of numbers for which you want info):
The secrets files are located in the following folders:
  1. Storage
  2. Server
  3. Transcription
  4. Call
 You want to copy secrets sample and then fill in the blanks.  You will need to set up your own API keys.

## create a screen to run the three different components of the project
screen -S <screen_name>
python3 runners.py
<CTRL A-D> 

screen -S <screen_name>
python3 start_server.py --twilio_prod
<CTRL A-D>

screen -S <screen_name>
python3 start_server.py --admin_prod
<CTRL A-D>

[<CTRL A-D> exits but does not terminate the screen]
[screen -r <screen_name> returns to the screen to check the status]
[<CTRL D> terminates the screen]

## Accessing the admin:
<server_ip>:8080/admin

