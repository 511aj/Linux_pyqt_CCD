# 这是linux胶体金检测项目
# 项目介绍
## linux4.13 + pyqt5
# 要安装的库

## 嵌入式linux系统
```python
pip install qtpy

pip install paho.mqtt 

pip install flask

pip install sqlite
```



## 设置环境变量

```bash
# 字体
export QT_QPA_FONTDIR=/usr/share/fonts/wqy-zenhei/
# 设置显示插件
export QT_QPA_PLATFORM=linuxfb
```

## 设置时间

```bash
# 设置中国时区
ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
```

```bash
ntpdate ntp1.aliyun.com
```



# 系统初始化



```bash
# 创建wifi模块驱动文件夹
mkdir  /lib/firmware/rtlwifi  -p
# 复制文件
cp  rtl8188eufw.bin  /lib/firmware/rtlwifi 

# wifi 配置文件
cp wpa_supplicant.conf /etc/wpa_supplicant.conf

cp r8188eu.ko /root
cp wifi.sh /root


vi /etc/profile
>>增加以上环境变量
```



## 自动登录

```bash
启动系统后， 
vi /etc/inittab 
#找到 /etc/inittab 文件的 
console::respawn:/sbin/getty -L  console 0 vt100 # GENERIC_SERIAL 
#修改为： 
console::respawn:-/bin/sh 
# 重启
```







/etc/rc.local

```bash
#!/bin/sh

# 自动启动WiFi

/root/wifi.sh

# 等待网络稳定

sleep 5

# 启动Python程序

cd /root/Linux_pyqt_CCD/main/
python3 main.py >> /tmp/myapp.log 2>&1 &


```



## 服务器端

```bash
# MEQX 
# MYSQL

pip install flask
pip install paho.mqtt    
pip install pymysql (数据库，这是服务器后端的，还需要前面安装的flask库，mqtt库)


```