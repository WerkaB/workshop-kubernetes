# Kubernetes workshop - DEMO application

## Environment variables for shrek and translate applications

### shrek

- env variable - QUOTES_PATH

### translate

- env variable - FUN bool type
- env variable - SHREK_SERVICE_URL string type

## Run containers in docker

``` bash
docker pull python:latest
docker pull busybox
docker build -t shrek:latest .
docker run -d -p 5000:5000 --name=shrek shrek:latest
docker container ls -a
docker inspect <nazwa-kontenera>
curl http://0.0.0.0:5000/shrek
curl http://0.0.0.0:5000/donkey

docker build -t translate:latest .
docker run -d -p 8080:8080 --name=translate --env=FUN=True --env=SHREK_SERVICE_URL="http://172.18.0.2:5000" translate:latest
curl http://0.0.0.0:8080/translate-shrek
curl http://0.0.0.0:8080/translate-donkey

git clone https://github.com/WerkaB/workshop-kubernetes.git

curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
kubectl create ns werka
kubectl config current-context
kubectl config set-context --current --namespace=werka
minikube image load my-image
```

## From workshop 12.2023

``` bash
docker pull python:latest
docker pull busybox
git clone https://github.com/WerkaB/workshop-kubernetes.git
cd workshop-kubernetes
cd shrek
docker build -t shrek:latest .
cd ../translate
docker build -t translate:latest .
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
minikube start --force
minikube image load shrek
minikube image load translate
cd ..
```

### For cm and deploy creation

``` bash
mkdir yaml
cd yaml
kubectl create deploy SHREK --image=shrek:latest --replicas=1 --output=yaml --dry-run=client >> shrek.deploy.yaml
kubectl create deploy TRANSLATE --image=translate:latest --replicas=1 --output=yaml --dry-run=client >> translate.deploy.yaml
cd ../shrek/
kubectl create cm shrek-cm --from-file=quotes.json --output=yaml --dry-run=client >> ../yaml/shrek-cm.yaml
```

## For Projekt Innowacje

We use "Kubernetes Sandbox" on O'Reilly

``` bash
docker pull python:latest
docker pull busybox
git clone https://github.com/WerkaB/workshop-kubernetes.git
cd workshop-kubernetes/shrek
docker build -t shrek:latest .
cd ../translate
docker build -t translate:latest .
cd ../../

# Copy shrek image
docker image save shrek:latest --output=shrek.tar
scp shrek.tar root@node01:~
ssh node01
sudo ctr -n=k8s.io images import shrek.tar # instead of: docker image load --input=shrek.tar
exit

# Copy translate image
docker image save translate:latest --output=translate.tar
scp translate.tar root@node01:~
ssh node01
sudo ctr -n=k8s.io images import translate.tar # instead of: docker image load --input=translate.tar
exit

kubectl run shrek --image=shrek:latest --dry-run=client -o yaml --restart=Never > pod_shrek.yaml
vim pod_shrek.yaml  # Change the spec.template.spec.containers[].imagePullPolicy: Never
kubectl apply -f pod_shrek.yaml

# Deployment of the ready application
cd workshop-kubernetes
kubectl apply -f -f ./yaml

kubectl get po -w
kubectl expose deploy shrek --port=5000 --target-port=5000
kubectl expose deploy translate --port=8000 --target-port=8080

kubectl run test --image=alpine:3.22.0 --restart=Never -- sleep 3600
kubectl exec -ti test -- sh
curl shrek.default.svc.cluster.local:5000/shrek
curl shrek.default.svc.cluster.local:5000/donkey
curl translate.default.svc.cluster.local:5000/translate-shrek
```