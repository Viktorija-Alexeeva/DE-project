# DE-project
Final project has been created during Data Engineering Zoomcamp. 

1. create repo 'DE-project' in github.

2. create new project 'airbnb-prices' in GCP.
enable Compute Engine API. 

generate ssh key for VM.

in bash in /.ssh folder
```
ssh-keygen -t rsa -f proj -C viktorija -b 2048

cat proj.pub
```

in gcp Metadata - ssh keys - add ssh key. copy there public key (result of cat proj.pub)

3. create VM instance 'de-project'.
copy external IP, then connect to VM for the first time. 

in bash:
```
ssh -i ~/.ssh/proj viktorija@34.79.46.252
```

4. in .ssh/config file add info about new ssh connection. 
Host de-project
    HostName 34.79.46.252
    User viktorija
    IdentityFile C:\Users\User\.ssh\proj 

5. clone repo on remote VM: 

in bash: 
```
$ git clone https://github.com/Viktorija-Alexeeva/DE-project.git
```

6. download anaconda (link from google)

in bash:
```
wget https://repo.anaconda.com/archive/Anaconda3-2024.10-1-Linux-x86_64.sh

bash Anaconda3-2024.10-1-Linux-x86_64.sh
```

7. install terraform.
copy link in google for Amd64. 

in bash: in bin/
```
wget https://releases.hashicorp.com/terraform/1.11.1/terraform_1.11.1_linux_amd64.zip

sudo apt-get install unzip

unzip terraform_1.11.1_linux_amd64.zip
rm terraform_1.11.1_linux_amd64.zip
```

8. create terraform-runner service account in gcp. 
name: terraform-runner
roles:  BigQuery Admin
        Compute Admin
        Dataproc Administrator
        Storage Admin
add key in .json. 
copy key into:
-  .gc/airbnb.json (on premises)
- create folder .keys/airbnb.json (remote)


5. Google Cloud SDK Authentication
in bash:
```
export GOOGLE_APPLICATION_CREDENTIALS=~/.gc/ny-rides.json
```


6. using terraform, create new bucket and dataset.  

