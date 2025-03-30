Steps to setup environment for project 'airbnb-prices-eu'.

1. Create repo 'DE-project' in github.

2. Create new project 'airbnb-prices-eu' in GCP.

Enable Compute Engine API. 

Generate ssh key for VM:

In bash in /.ssh folder:
```
ssh-keygen -t rsa -f proj-vm -C viktorija -b 2048
cat proj-vm.pub
```

In GCP Metadata - ssh keys - add ssh key. Copy there public key (result of cat proj-vm.pub).

3. Create VM instance 'de-project' in GCP.

In GCP Compute Engine - VM instances - create. 
```
name: de-project
location: europe-west1-b
machine type: e2-standard-4 (4 vCPUs, 16 GB Memory)
image: ubuntu2004
```
Start VM instance. 

Copy external IP, then connect to VM for the first time: 

In bash:
```
ssh -i ~/.ssh/proj-vm viktorija@34.38.125.214
```

4. In .ssh/config file add info about new ssh connection. 
```
Host de-project
    HostName 34.38.125.214
    User viktorija
    IdentityFile C:\Users\User\.ssh\proj-vm
```

5. Clone git repo on remote VM. 

In bash: 
```
$ git clone https://github.com/Viktorija-Alexeeva/DE-project.git
```

Configure username and email in git: 

In bash in DE-project/:
```
git config --local user.name "Your Name"
git config --local user.email "your-email@example.com"
```
Change ownership of directory:

In bash:
```
sudo chown -R viktorija:viktorija ~/DE-project
```

Configure VS code to access VM.

In VS code: extensions - remote SSH - install - open a remote window (click on button on the left corner) - connect to host - de-project. 

6. Install Anaconda (link from google).

In bash:
```
wget https://repo.anaconda.com/archive/Anaconda3-2024.10-1-Linux-x86_64.sh
bash Anaconda3-2024.10-1-Linux-x86_64.sh
```

7. Install Terraform (link from google).

In bash in /bin:
```
wget https://releases.hashicorp.com/terraform/1.11.1/terraform_1.11.1_linux_amd64.zip

sudo apt-get install unzip
unzip terraform_1.11.1_linux_amd64.zip
rm terraform_1.11.1_linux_amd64.zip
```

8. Create terraform-runner service account in GCP.

In GCP IAM & Admin - Service accounts - create.
```
name: terraform-runner
roles:  BigQuery Admin
        Compute Admin
        Storage Admin
```
For created account add key in .json. 

On premises copy key into /.gc/prices.json.

Copy key to server:

In bash in /.gc folder:
```
sftp de-project
mkdir .gc/
cd .gc
put prices.json
```

Add to .bashrc for default authentication:
```
export GOOGLE_APPLICATION_CREDENTIALS=~/.gc/prices.json
gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
```

9. Install Docker.

In bash:
```
sudo apt-get update
sudo apt-get install docker.io
sudo groupadd docker
sudo gpasswd -a $USER docker
sudo service docker restart
```
Then logout and login again. Check that Docker works:

In bash:
```
docker run hello-world
```

10. Install docker-compose. 

In google: https://github.com/docker/compose/releases/tag/v2.33.1.
Copy link of 'docker-compose-linux-x86-64'.

In bash in bin/:
```
wget https://github.com/docker/compose/releases/download/v2.33.1/docker-compose-linux-x86_64 -O docker-compose
chmod +x docker-compose
```

11. Create separate dataset for development environment of DBT project.

In BQ create dataset: 
```
name: airbnb_prices_eu_dev
location: europe-west1
```

Now you are ready to reproduce the project. Follow instructions in file 'reproduce.md'. 


