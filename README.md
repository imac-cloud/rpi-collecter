# Collect Sensor Data Using Raspberry Pi
透過 Raspberry Pi 與簡單幾個感測器來實作資料的收集，並推送到 OpenStack 上的 MQTT Broker、Apache Kafka伺服器。也可以透過 Spark Streaming 來接收 MQTT 與 Kafka 的訊息，目前實作以下感測器的接收：
* DS18B20 溫度感測器

訊息佇列系統的推送目前實作```MQTT```與```Apache Kafka```，未來也會持續增加。

# 安裝與執行
首先安裝 python 與 python-pip 套件：
```sh
$ sudo apt-get install -y git python-pip
```

從 Git Server 將 Repositiory 下載至要執行的 Raspberry Pi 上：
```sh
$ git clone https://github.com/imac-cloud/rpi-collecter.git
$ cd rpi-collecter
```

建立 conf 目錄，並複製 conf 檔案到 etc 底下：
```sh
$ SERVICE="rpi-collecter"
$ sudo mkdir -p /etc/${SERVICE}
$ sudo chown -R ${SERVICE}:${SERVICE} /etc/${SERVICE}
$ sudo cp -r etc/rpi-collecter/rpi-collecter.conf /etc/${SERVICE}/
```

安裝```rpi-collecter```服務套件：
```sh
$ sudo pip install .
```
> 也可以透過以下方式安裝：
```sh
$ sudo python setup.py install
```

編輯```/etc/rpi-collecter/rpi-collecter.conf```檔案，並修改一下：
```conf
[default]
sensor_id_path = /sys/bus/w1/devices/28-00000758ff7b/w1_slave
time_interval = 1

[message_queue]
type = mqtt
address = localhost
port = 1883
topic_name = rpi-1
qos_level = 2
```
> ```P.S``` 目前 message_queue type 有```mqtt```、```kafka```。若沒設定則不會推送。

完成後，即可透過以下指令執行（目前還沒完成 Service 方式執行）：
```sh
$ rpi-collector

[Temperature][INFO] 2016-03-10 15:58:12.315205, 23.75
[Temperature][INFO] 2016-03-10 15:58:13.339659, 23.75
[Temperature][INFO] 2016-03-10 15:58:14.360168, 23.75
[Temperature][INFO] 2016-03-10 15:58:15.369965, 23.75
```
