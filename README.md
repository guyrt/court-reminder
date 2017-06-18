All info at: https://github.com/guyrt/court-reminder/

## court-reminder - what it does
Calling things and transcribing.  

Here we have instructions for running the program on a local machine and on an Azure VM.

# Install github on your computer
go to www.github.com in order to install git

# Running on local machine 
## Clone the court reminder repository
Open a terminal on your computer.  
Navigate to the directory you would want your new directory to be:
e.g. cd C:\Users\yourname\
Then clone github repo:
Go to https://github.com/guyrt/court-reminder/ and click on the green Clone or download button.  Copy the url. 
In your terminal, type:
git clone <url>

## install python 3 and some other things
### For ubuntu
sudo apt-get update (you will have to enter the password for your machine)
sudo apt-get install python-dev build-essential libssl-dev libffi-dev python3-pip libffi-dev -y
### For windows
Install anaconda: https://www.continuum.io/downloads
### For Mac
xcode-select --install
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew doctor
"Once you’ve installed Homebrew, insert the Homebrew directory at the top of your PATH environment variable. You can do this by adding the following line at the bottom of your ~/.profile file
export PATH=/usr/local/bin:/usr/local/sbin:$PATH
" (from http://python-guide-pt-br.readthedocs.io/en/latest/starting/install3/osx/)
brew install python3

## install modules that are needed
sudo pip3 install -r requirements.txt
### For ubuntu
sudo apt-get install sox -y
### For windows
download sox from their website
### For Mac
brew install sox

## Fill in secrets files (these contain API keys, lists of numbers for which you want info):
You will need to set up accounts with the various services that we use (Twilio, Google Clound, Azure Storage table).  
You will then need to fill in the various secrets files with your credentials for these accounts.  Copy secrets sample and then fill in the blanks.  (cp secrets.sample.py secrets.py)
The secrets files are located in the following folders:

  1. Call -- ~\CourtHearings\court-reminder\call\secrets.py
  To fill out this information, you first need a Twilio account. Set up one at www.twilio.com.  Then edit the fields in the secret file: ~\CourtHearings\court-reminder\call\secrets.py
  Your AccountSid and AuthToken can be found on your Account Dashboard. 
 
  2. Storage -- ~\CourtHearings\court-reminder\storage\secrets.py
  We use an Azure storage account for this.  Here are instructions on how to set up an Azure storage account. 
  https://docs.microsoft.com/en-us/azure/storage/storage-create-storage-account#create-a-storage-account
  You will want to set up one general table and one blob storage table
  
  3. Transcription  ~\CourtHearings\court-reminder\transcribe\secrets.py
  Here are instructions to get started with the google cloud speech API here:
  https://cloud.google.com/speech/docs/getting-started
  
  
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

