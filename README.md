# Collect Sensor Data Using Raspberry Pi
透過 Raspberry Pi 與簡單幾個感測器來實作資料的收集，並推送到 OpenStack 上的 MQTT Broker、Apache Kafka伺服器。也可以透過 Spark Streaming 來接收 MQTT 與 Kafka 的訊息，目前實作以下感測器的接收：
* DS18B20 溫度感測器

訊息佇列系統的推送目前實作```MQTT```與```Apache Kafka```，未來也會持續增加。

# 安裝與執行
首先安裝 python 與 python-pip 套件：
```sh
$ sudo apt-get install -y git python-pip python-setuptools
```

從 Git Server 將 Repositiory 下載至要執行的 Raspberry Pi 上：
```sh
$ git clone https://github.com/imac-cloud/rpi-collector.git
$ cd rpi-collector
```

建立 conf 目錄，並複製 conf 檔案到 etc 底下：
```sh
$ SERVICE="rpi-collector"
$ sudo mkdir -p /etc/${SERVICE}
$ sudo chown -R ${SERVICE}:${SERVICE} /etc/${SERVICE}
$ sudo cp -r etc/rpi-collector/rpi-collector.conf /etc/${SERVICE}/
```

安裝```rpi-collecter```服務套件：
```sh
$ sudo pip install .
```
> 也可以透過以下方式安裝：
```sh
$ sudo python setup.py install
```

編輯```/etc/rpi-collector/rpi-collector.conf```檔案，並修改一下：
```conf
[default]
w1therm_sensors_id = 28-00000758e2c2
w1therm_sensors_type = DS18S20
time_interval = 1

[message_queue]
type = mqtt
address = 10.21.20.195
port = 1883
topic_name = bridge/rpi-1
qos_level = 2
```
> ```P.S``` 目前 message_queue type 有```mqtt```、```kafka```。若沒設定則不會推送。

完成後，即可透過以下指令執行（目前還沒完成 Service 方式執行）：
```sh
$ rpi-collector
[collect.temperature][INFO] 2016-03-10 17:14:37.535571, 23.75
[collect.temperature][INFO] 2016-03-10 17:14:38.565419, 23.75
[collect.temperature][INFO] 2016-03-10 17:14:39.583886, 23.75
[collect.temperature][INFO] 2016-03-10 17:14:40.611681, 23.75
```
