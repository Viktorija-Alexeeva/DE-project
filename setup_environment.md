Steps to setup environment for project 'airbnb-prices-eu'.

1. create repo 'DE-project' in github.

2. create new project 'airbnb-prices-eu' in GCP.

enable Compute Engine API. 

generate ssh key for VM. 

in bash in /.ssh folder:
```
ssh-keygen -t rsa -f proj-vm -C viktorija -b 2048
cat proj-vm.pub
```

in gcp Metadata - ssh keys - add ssh key. copy there public key (result of cat proj-vm.pub)

3. create VM instance 'de-project'.
copy external IP, then connect to VM for the first time. 

in bash:
```
ssh -i ~/.ssh/proj-vm viktorija@34.38.125.214
```

4. in .ssh/config file add info about new ssh connection. 
```
Host de-project
    HostName 34.38.125.214
    User viktorija
    IdentityFile C:\Users\User\.ssh\proj-vm
```

5. clone git repo on remote VM: 

in bash: 
```
$ git clone https://github.com/Viktorija-Alexeeva/DE-project.git
```

configure username and email in git: 

in bash in DE-project/:
```
git config --local user.name "Your Name"
git config --local user.email "your-email@example.com"
```
change ownership of directory:
in bash:
```
sudo chown -R viktorija:viktorija ~/DE-project
```

6. install anaconda (link from google).

in bash:
```
wget https://repo.anaconda.com/archive/Anaconda3-2024.10-1-Linux-x86_64.sh
bash Anaconda3-2024.10-1-Linux-x86_64.sh
```

7. install terraform.
copy link in google for Amd64. 

in bash: in /bin:
```
wget https://releases.hashicorp.com/terraform/1.11.1/terraform_1.11.1_linux_amd64.zip

sudo apt-get install unzip
unzip terraform_1.11.1_linux_amd64.zip
rm terraform_1.11.1_linux_amd64.zip
```

8. configure terraform files. 
in folder DE-project/terraform create and configure files main.tf and variables.tf.

9. create terraform-runner service account in gcp. 
```
name: terraform-runner
roles:  BigQuery Admin
        Compute Admin
        Dataproc Administrator
        Storage Admin
```
add key in .json. 
on premises copy key into:
- .gc/prices.json (on premises and for gcloud)
- create folder DE-project/.keys/prices.json (and copy to remote for another cases)

to copy key to server:
in bash: in /.gc folder:
```
sftp de-project
mkdir .gc/
cd .gc
put prices.json
```

add to .bashrc for default authentication:
```
export GOOGLE_APPLICATION_CREDENTIALS=~/.gc/prices.json
gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
```

10. install docker.
in bash:
```
sudo apt-get update
sudo apt-get install docker.io
sudo groupadd docker
sudo gpasswd -a $USER docker
sudo service docker restart
```
then logout and login again. and check that docker works.

in bash:
```
docker run hello-world
```

11. install docker-compose. 
in google: https://github.com/docker/compose/releases/tag/v2.33.1.
copy link of 'docker-compose-linux-x86-64'

in bash in bin/:
```
wget https://github.com/docker/compose/releases/download/v2.33.1/docker-compose-linux-x86_64 -O docker-compose
chmod +x docker-compose
```

12. install java.
create ~/spark folder.
download OpenJDK.
in bash in /spark:
```
wget https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz
tar xzfv openjdk-11.0.2_linux-x64_bin.tar.gz
rm openjdk-11.0.2_linux-x64_bin.tar.gz
```
define JAVA_HOME and add it to PATH:
in bash in /spark:
```
export JAVA_HOME="${HOME}/spark/jdk-11.0.2"
export PATH="${JAVA_HOME}/bin:${PATH}"
```

13. install spark.
in bash in /spark:
```
wget https://archive.apache.org/dist/spark/spark-3.5.5/spark-3.5.5-bin-hadoop3.tgz
tar xzfv spark-3.5.5-bin-hadoop3.tgz
rm spark-3.5.5-bin-hadoop3.tgz
```
Add it to PATH:
in bash in /spark:
```
export SPARK_HOME="${HOME}/spark/spark-3.5.5-bin-hadoop3"
export PATH="${SPARK_HOME}/bin:${PATH}"
```
check that spark works:
in bash in /spark:
```
spark-shell
val data = 1 to 10000
val distData = sc.parallelize(data)
distData.filter(_ < 10).collect()
```

to connect to GCS need to downlod jar:
in bash in DE-project/code:
```
mkdir lib
cd lib
gsutil cp gs://hadoop-lib/gcs/gcs-connector-hadoop3-2.2.5.jar gcs-connector-hadoop3-2.2.5.jar
```

14. add java and spark paths into .bashrc:
in bash:
```
nano .bashrc
```

go to the end of file and add:
```
export JAVA_HOME="${HOME}/spark/jdk-11.0.2"
export PATH="${JAVA_HOME}/bin:${PATH}"

export SPARK_HOME="${HOME}/spark/spark-3.5.5-bin-hadoop3"
export PATH="${SPARK_HOME}/bin:${PATH}"
```
CTRL + O
CTRL + X

apply changes immediately:
in bash:
```
source .bashrc
```

15. configure connection to Kestra with docker-compose. 
in DE-project/kestra create and configure :
- docker-compose.yaml to configure Kestra and Kestra-metadata containers connection together in 1 file. 
- gcp_kv.yaml to pass kv parameters to kestra.

in VS add forwarded ports: 8080 and 8081.

in bash in /kestra:
```
docker-compose up -d
```
then in google open http://localhost:8080 - will open Kestra UI. 

Flows - create - copy code from gcp_kv.yaml - save - execute.
after execution in Namespaces - de-project - kv store -  will appear 4 keys. 

16. create flow to upload csv files into gcs bucket.  
in DE-project/kestra folder create upload_data_to_gcs.yaml file.
It will:
- download 'visualisations/listings.csv' files from "https://insideairbnb.com/get-the-data/"
- rename csv files as: {country}_{region}_{city}_{release_date}_listings.csv
- add 4 additional columns: country, region, city, release_date
- upload updated csv files into gcs bucket into {country} folder

 
