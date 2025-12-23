# Памятка

## Разверните Strimzi, используя установочные файлы

```bash
kubectl create namespace kafka
kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka

kubectl get pod -n kafka --watch
kubectl logs deployment/strimzi-cluster-operator -n kafka -f
```

## Создайте кластер Apache Kafka

```bash
kubectl apply -f https://strimzi.io/examples/latest/kafka/kafka-single-node.yaml -n kafka

kubectl wait kafka/my-cluster --for=condition=Ready --timeout=300s -n kafka
```

## Отправляйте и получайте сообщения

```bash
kubectl -n kafka run kafka-producer -ti --image=quay.io/strimzi/kafka:0.49.1-kafka-4.1.1 --rm=true --restart=Never -- bin/kafka-console-producer.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --topic my-topic
kubectl -n kafka run kafka-consumer -ti --image=quay.io/strimzi/kafka:0.49.1-kafka-4.1.1 --rm=true --restart=Never -- bin/kafka-console-consumer.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --topic my-topic --from-beginning
 ```

## Удаление кластера Apache Kafka

```bash
kubectl -n kafka delete $(kubectl get strimzi -o name -n kafka)
kubectl delete pvc -l strimzi.io/name=my-cluster-kafka -n kafka
```

## Удаление кластерного оператора Strimzi

```bash
kubectl -n kafka delete -f 'https://strimzi.io/install/latest?namespace=kafka'
kubectl delete namespace kafka
```
