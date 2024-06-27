AWS DEPLOYEMENT
1) Login to AWS console : https://aws.amazon.com/console/
2) Search for EC2
3) Config UBUNTU machine
4) Launch instance
5) Update machine

   sudo apt update

   sudo apt-get update

   sudo apt upgrade -y

   sudo apt install git curl unzip tar make sudo vim wget -y

6) Git clone this repository

   git clone repository_link

7) sudo apt install python3-pip
8) pip3 install -r requirements.txt
9) Go with security and add inbound rule with port as 8051, source as 0.0.0.0/0, type as Custom-TCP 
10) python3 -m streamlit run StreamlitAPP.py



If you want to add OpenAI api key :
1) Create .env file in your server

   touch.env

2) vi .env
3) Press insert
4) Copy your API key and paste it there
5) Press esc to save it
6) Type :wq and press enter to exit file editor and return back to terminal



   
