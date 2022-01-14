# 居家環境遠端管理 - 以樹莓派實作
 
## 目的
   透過樹苺派及Python架構一個原型(prototype)，可以透過Internet(Web/LINE)取得終端設備(eg.鏡頭、感測裝置、電器)之數據或控制。
  
## 硬體設備需求
   1. 樹莓派 * 1
   2. [NOIR 鏡頭](https://safe.menlosecurity.com/https://www.uctronics.com/raspberry-pi-noir-camera-board-w-cs-mount-lens-compatible-with-official-module.html) * 1
   3. [DHT22](https://www.raspberrypi.com.tw/23140/dht22-temperature-and-humidity-sensor/) 溫溼度感測模組 * 1
   4. [紅外線接收模組](https://maker.pro/raspberry-pi/tutorial/how-to-interface-a-pir-motion-sensor-with-raspberry-pi-gpio) * 1
   5. 麵包版/印刷電路板/Led/電阻/杜邦線 (視線路規劃而定)
   6. 40Pins彩虹排線 / [T-Cobbler](https://www.adafruit.com/product/2028) * 1
   7. 簡易焊接設備(若不想把所有線路透過麵包版連接再一起)
   8. 七段顯示器 * 1 (純為測試與噱頭用，可有可無)
   9. 紙箱或薄木板(固定相關設備，方便移動及避免電路鬆脫)
## 軟體及環境需求
   1. VNC viewer
## 建議及注意事項

   1. 為確保系統Python程式除錯過程順利，會先完成電路接線，並透過簡易程式確認GPIO 各項接點控制led，方便確認能夠正常運作，才進行Python 程式撰寫。
   2. 實作過程中，為了測試除錯，在樹莓派上面插拔一堆線路接是件很不方便的事，購過40pins排線轉接到麵包版上的T-Cobbler 可以改善工作效率。
   3. 鏡頭及紅外線體感偵測器(PIR)怕靜電，接線過程中要確定完成去除靜電。
   4. PIR接線前要確認三根接腳哪支接腳是接地(GND)，可以把白色遮罩蓋拿起來確認。為了實作過程方便測試，可調整紅外線偵測器的靈敏度(SX)調高, 延遲時間(TX)調低。(順時針方向都是調高)
   5. 
## 過程及步驟

### 系統架構如下圖，此實作前提是樹莓派已經完成基本環境設定，接下來要完成的主要步驟如下:

#### 終端硬體設備及電路
  + 電路圖如下。
  
	![GPIO.jpg](https://github.com/molin-lin/Image/blob/main/GPIO.jpg "GPIO.jpg")
  
  + [GPIO.jpg](https://www.raspberrypi.com/documentation/computers/os.html)其各[針腳接線](https://pinout.xyz/)與相關感測模組對應如下。

  | GIPO Pin number| Description      |GIPO Pin number| Description               |
  | ------------- | ----------------- |  ------------- | ------------------------- | 
  | `3V3 power`   |   **DHT22 PWR**       | `(02)5V power `  | **Used for 7 segments display**  |
  | `(01)GPIO 2`   | **LED (PIR)**       | `(04)5V power`  | NIL     |
  | `(03)GPIO 3`   | **DHT22 Data INPT** | `(06)GND `      | NIL     |
  | `(05)GPIO 4`   | **PIR DATA INPT**   | `(08)GPIO 14`   | NIL    |
  | `(07)GND `     | NIL     | `(10)GPIO 15 `   | NIL    |
  | `(11)GPIO 17 ` | NIL     | `(12)GPIO 18` | NIL     |
  | `(13)GPIO 27 ` | NIL     | `(14)GND`   | NIL     |
  | `(15)GPIO 22`   | NIL     | `(16)GPIO 23`   | NIL     |
  | `(17)3.3V`    | NIL     | `(18)GPIO 24`   | NIL       |
  | `(19)GPIO 10 `   | NIL     | `(20)GND`   | NIL     |
  | `(21)GPIO 9 `   | NIL     | `(22)GPIO 25`   | NIL     |
  | `(23)GPIO 11 `   | NIL     | `(24)GPIO 8`   | NIL     |
  | `(25)GND `   | NIL     | `(26)GPIO 7`   | NIL     |
  | `(27)GPIO 0`   | NIL     | `(28)GPIO 1 `   | NIL     |
  | `(29)GPIO 5`   | NIL     | `(30)GND`   | NIL     |
  | `(31)GPIO 6`   | NIL     | `(32)GPIO 12`   | NIL     |
  | `(33)GPIO 13`   | NIL     | `(34)GND`   | NIL     |
  | `(35)GPIO 19`   | NIL     | `(36)GPIO 16`   | NIL     |
  | `(37)GPIO 26`   | NIL     | `(38)GPIO 20`   | NIL    |
  | `(39)GND`   | **GND for ALL devices**  | `(40)GPIO 21`   | NIL     |
  

#### 系統開發建置。
  + 系統開發個人的習慣是從單一功能function開始,利用簡單的python程式進行電路控制測試，沒有問題後再整合一起。本實作分成如下幾個部分。
  	+ 紅外線PIR功能及單元測試
  	+ 溫溼度感測功能及單元測試
            + 安裝python 套件
              執行指令 `sudo pip3 install Adafruit_DHT`
  	+ 鏡頭模組功能及單元測試
  	    + 安裝python套件
  	      執行指令: `pip install opencv-python`
  	+ Web 網頁 (Flask)開發及測試
  	+ Ngrok 功能建置及單元測試
  	+ LINE Bot 功能
  + 有關 flask、ngrok、LINE Developers 相關安裝細節可參考如下連結內容進行。
  	+ 網站的架設(本實作是透過 [Flask](https://flask.palletsprojects.com/en/2.0.x/))。
  	+ 樹莓派能夠透通到internet(本實作是採用[ngrok](https://ithelp.ithome.com.tw/articles/10197345))，提供URL 給外面(web/LINE)來連結使用。
  	+ LiNE 機器人(Bot) 的申請與設定可透過 [LINE Developers](https://developers.line.biz/zh-hant/docs/messaging-api/getting-started/)依步驟完成。


*. 安裝 Flask (網站開方框架函式庫)

*. setup camera for python 
   執行指令: `pip install opencv-python`


*. Create practice_app.py
*. python3 practice_app.py  


*. Setup ngrok

	a. https://dashboard.ngrok.com/get-started/setup

*. Setup environment
	b. get authtoken
	c. ./ngrok authtoken [token]
	d. ./ngrok http 5000

*安裝 LINE Bot SDK
  執行指令：`pip3 install line-bot-sdk`
![LINE](https://www.flickr.com/photos/194854339@N08/shares/ZyM56N "LINE")

*Setup message API via Line developers,	https://developers.line.biz/console/

*setup environment paramenters
	export LINE_CHANNEL_SECRET=
	export LINE_CHANNEL_ACCESS_TOKEN=

	**LINE_CHANNEL_SECRET =
	**LINE_CHANNEL_ACCESS_TOKEN=



Run Steps

step1: get ngrok token, https://dashboard.ngrok.com/auth
step2: start terminal, ./ngrok authtoken[token]
step3: build the channel, 
	>./ngrok http [port] , port=5000 in this pratice.
	We can get the forwarding URL from the response message.
	
step4: setup Web Server using Python, and the port must be the same with ngrok, 
	>python -m SimpleHTTPServer [port] , port=5000 in this pratice.

step5: run web_app in command mode, 
	>python3 web_app.py  


## 成果示範

## 改善方向與心得

## 參考資料
[1]. [人體紅外線偵測](https://tutorials.webduino.io/zh-tw/docs/socket/sensor/pir.html "人體紅外線偵測") <br>
[2]. [教你如何使用Python成功串接Linebot(2020版)](https://ithelp.ithome.com.tw/articles/10229943"教你如何使用Python成功串接Linebot(2020版)") <br>
[3]. [Python+LINE Bot教學 6步驟快速上手LINE Bot機器人](https://www.learncodewithmike.com/2020/06/python-line-bot.html "Python+LINE Bot教學 6步驟快速上手LINE Bot機器人") <br>
[4]. [Messaging API 介紹](https://developers.line.biz/zh-hant/docs/messaging-api/overview/ "Messaging API 介紹") <br>
[5]. [樹莓派連接DHT22偵測溫濕度](https://ithelp.ithome.com.tw/articles/10238029 "樹莓派連接DHT22偵測溫濕度")<br>
[6].

