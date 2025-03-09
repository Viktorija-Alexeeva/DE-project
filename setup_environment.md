Steps to setup environment for project 'airbnb-prices'.

1. create repo 'DE-project' in github.

2. create new project 'airbnb-prices' in GCP.
enable Compute Engine API. 

generate ssh key for VM.
in bash in /.ssh folder:
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
```
Host de-project
    HostName 34.79.46.252
    User viktorija
    IdentityFile C:\Users\User\.ssh\proj 
```

5. clone git repo on remote VM: 

in bash: 
```
$ git clone https://github.com/Viktorija-Alexeeva/DE-project.git
```

6. download anaconda (link from google).

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
in folder DE-project/terraform create and configure files main.tf and varibles.tf.

9. create terraform-runner service account in gcp. 
```
name: terraform-runner
roles:  BigQuery Admin
        Compute Admin
        Dataproc Administrator
        Storage Admin
```
add key in .json. 
copy key into:
- .gc/airbnb.json (on premises and for gcloud)
- create folder .keys/airbnb.json (remote for another cases)

to copy key to server:
in bash: in /.gc folder:
```
sftp de-project
mkdir .gc/
cd .gc
put airbnb.json
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

12. install Kaggle and authentificate. 

in bash:
```
pip install kaggle
```

set up kaggle API key.
in kaggle account - settings - create new token - will download kaggle.json file.
save kaggle.json in ~/.kaggle/kaggle.json.

to copy key to server:
in bash: in /.kaggle folder:
```
sftp de-project
mkdir .kaggle/
cd .kaggle
put kaggle.json
```
Set permissions:
in bash: 
```
chmod 600 ~/.kaggle/kaggle.json
```

13. install java.
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

14. install spark.
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

add java and spark paths into .bashrc:
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

15. setup Dataproc cluster in gcp.
enable Dataproc API. 
create cluster:
```
name: de-project-cluster
location: europe-west1
zone: europe-west1-b
cluster type: single node.
optional components: jupyter notebook and docker. 
```
will be created: 
- cluster: 'de-project-cluster'
- VM 'de-project-cluster-m'
- 2 buckets: 'dataproc-temp' and 'dataproc-staging'

16. create script to rearrange csv files in gcs bucket.  
in /code folder create upload_csv_to_gcs.py file.
It will divide files into 2 folders (under csv/): weekends and weekdays.

