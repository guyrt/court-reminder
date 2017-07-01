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
git clone &lt; url &gt;

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
  The deployment model is resource manager, and you will want to create a General Purpose with performance tier standard.  Store the name of the storage_account in the storage_account variable in the secrets file.  Go to the access keys tab, and set Key1 in the variables blob_key and table_connection_string.
Next, go to "blob store" from overview and create a container. Store the name of this container in the variable blob_container. 
Next, set table_name = "courtreminder" in secrets.py. Our code will make the table for you. 
Note that the db_* variables shouldn't be used
  
  3. Transcription  ~\CourtHearings\court-reminder\transcribe\secrets.py
  Here are instructions to get started with the google cloud speech API here:
  https://cloud.google.com/speech/docs/getting-started
  Create a new project.  Give it a name. 
  Go to API manager, then click on credentials
  Click create credentials, and choose Service Account Key
  Choose your project as the service account and then download the json.  
  Copy the json into secrets.py. Don't do anything for the Bing speech recognition credentials (we used to use Bing, then we switched to Google).  You don't need to enter anything in the preferred phrases line either.
  
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
ssh &lt; username &gt; @ &lt; IP address &gt;

## Clone the court reminder repository
git clone &lt; court reminder repo &gt;

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
screen -S &lt; screen_name &gt;
python3 runners.py
&lt; CTRL A-D &gt;

screen -S &lt; screen_name &gt;
python3 start_server.py --twilio_prod
&lt; CTRL A-D &gt;

screen -S &lt; screen_name &gt;
python3 start_server.py --admin_prod
&lt; CTRL A-D &gt;

[&lt; CTRL A-D &gt; exits but does not terminate the screen]
[screen -r &lt; screen_name &gt; returns to the screen to check the status]
[&lt; CTRL D &gt; terminates the screen]

## Accessing the admin:
&lt; server_ip &gt; :8080/admin

