# 居家環境遠端管理 - 以樹莓派實作 (ver1.1 updated on 17/Jan/2022)
 
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

   1. 為確保系統Python程式除錯過程順利，會先完成電路接線，並透過簡易程式確認GPIO 各項接點控制 LED，方便確認能夠正常運作，才進行Python 程式撰寫。
   2. 實作過程中，為了測試除錯，在樹莓派上面插拔一堆線路接是件很不方便的事，購過40pins排線轉接到麵包版上的T-Cobbler 可以改善工作效率。
   3. 鏡頭及紅外線體感偵測器(PIR)怕靜電，接線過程中要確定完成去除靜電。
   4. PIR接線前要確認三根接腳哪支接腳是接地(GND)，可以把白色遮罩蓋拿起來確認。為了實作過程方便測試，可調整紅外線偵測器的靈敏度(SX)調高, 延遲時間(TX)調低。(順時針方向都是調高)
   
## 過程及步驟

### 系統架構如下圖，此實作前提是樹莓派已經完成基本環境設定，接下來要完成的主要步驟如下:

![msg_flow_1.jpg](https://github.com/molin-lin/Image/blob/main/msg_flow_1.jpg "msg_flow_1.jpg")


#### 終端硬體設備及電路
  + 電路圖如下。
  
	![circuit.png](https://github.com/molin-lin/Image/blob/main/circuit.png "circuit.png")
  
  + [GPIO](https://www.raspberrypi.com/documentation/computers/os.html)其各[針腳接線](https://pinout.xyz/)與相關感測模組對應如下。

  | GIPO Pin number| Description      |GIPO Pin number| Description               |
  | ------------- | ----------------- |  ------------- | ------------------------- | 
  | `(01)3V3 power`| **DHT22 PWR**       | `(02)5V power `  | **7 Seg. Disp. PWR**  |
  | `(03)GPIO 2`   | **LED (PIR)**       | `(04)5V power`   | NIL	 |
  | `(05)GPIO 3`   |                     | `(06)GND `       | NIL        |
  | `(07)GPIO 4`   | **DHT22 Data INPT** | `(08)GPIO 14`    | NIL        |
  | `(09)GND `     | NIL    		 | `(10)GPIO 15 `   | NIL        |
  | `(11)GPIO 17 ` | **PIR DATA INPT** 	 | `(12)GPIO 18`    | **顯示器-A**|
  | `(13)GPIO 27 ` | NIL		 | `(14)GND`        | NIL  	 |
  | `(15)GPIO 22`  | NIL   		 | `(16)GPIO 23`    | **顯示器-B**|
  | `(17)3.3V`     | NIL  		 | `(18)GPIO 24`    | **顯示器-C**|
  | `(19)GPIO 10 ` | NIL		 | `(20)GND`        | NIL        |
  | `(21)GPIO 9 `  | NIL   		 | `(22)GPIO 25`    | **顯示器-D**|
  | `(23)GPIO 11 ` | NIL 		 | `(24)GPIO 8`     | NIL   	 |
  | `(25)GND `     | NIL   		 | `(26)GPIO 7`     | NIL    	 |
  | `(27)GPIO 0`   | NIL		 | `(28)GPIO 1 `    | NIL   	 |
  | `(29)GPIO 5`   | NIL   		 | `(30)GND`        | NIL   	 |
  | `(31)GPIO 6`   | NIL  		 | `(32)GPIO 12`    | **顯示器-E**|
  | `(33)GPIO 13`  | NIL		 | `(34)GND`        | NIL        |
  | `(35)GPIO 19`  | NIL 		 | `(36)GPIO 16`    | **顯示器-F**|
  | `(37)GPIO 26`  | NIL  		 | `(38)GPIO 20`    | **顯示器-G**|
  | `(39)GND`      | **GND for ALL devices**  | `(40)GPIO 21`   | **LED**|
  

#### 系統開發建置。
  + 系統開發過程中，個人的習慣是從單一功能function開始,利用簡單的python程式進行電路控制測試，沒有問題後再一一整合。本實作分成如下幾個部分。
  	+ 紅外線PIR功能及單元測試
  	+ 溫溼度感測功能及單元測試
  	    + 安裝python 套件前，先確認系統已經更新。
		- [x] `sudo apt-get update` 
		- [x] `sudo apt-get install python3-pip`
		- [X] `sudo apt-get install python3-dev python3-pip`
		- [X] `sudo python3 -m pip install --upgrade pip setuptools wheel`
	    + 再安裝 Adafruit_DHT
	  
	      執行指令 `sudo pip3 install Adafruit_DHT`
  	+ 鏡頭模組功能及單元測試
  	    + 在安裝鏡頭套件前，有幾個關鍵套件要install，不然程式會卡關。
		- [x] `sudo apt-get install libatlas-base-dev` 
		- [x] `sudo apt-get install libjasper-dev`
		- [X] `sudo apt-get install libqtgui4`
		- [X] `sudo apt-get install python3-pyqt5`
  	    + 安裝 OpenCV
  	      執行指令: `pip3 install opencv-python`
	    + 若要確認鏡頭接線可正常運作，可透過指令 `raspistill -o image.png`  檢視照片內容確認鏡頭運作正常。

  	+ Web 網頁 (Flask)開發及測試
  	    + 安裝 Flask 基本套件(網站開方框架函式庫)
  	    
  	       `sudo pip3 install flask`
	       
  	+ Ngrok 功能建置及單元測試
  	    + 安裝 [Ngrok](https://dashboard.ngrok.com/get-started/setup) ，讓樹莓派的網站可透過ngrok 提供的internel URL 進行存取。
  	    + 設定樹莓派環境
  	        + 取得 authtoken

		`./ngrok authtoken [token]`
		
	        + 啟動 http port (port 需要跟 Flask 的 port 一致) 
	        
		`./ngrok http 5000`
	       
  	+ LINE Bot 功能
  	    + 首先安裝 LINE Bot SDK
  	    
	       執行指令: `pip3 install line-bot-sdk`
	       
	    
  	    + 想要透過 LNIE Bot跟樹莓派進行溝通，要先註冊LINE 官方帳號(目前免費)取得Provider，並建立Channel，才能開始設定並使用Message API。詳細步驟過程可參閱下一段的連結。
  	    + 這過程中需要紀錄幾個資料，是之後程式開發過程中會需要使用到的，當然可以透過 [LINE Developers Console](https://developers.line.biz/zh-hant/docs/messaging-api/getting-started/) 進行設定與取得相關資料。
                + Channel secret
                + Channel access token
                + 並於 Channel 設定頁面中，將「自動回應訊息」停用，並啟用「Webhook」。
                + 設定 Webhook URL，這項設定可從 ngrok 啟動後的畫面取得URL 後再來設定， 讓LINE platform 知道要連結到哪裡，並取得對應的response對應的response。


  + 有關 flask、ngrok、LINE Developers 相關安裝細節可參考如下連結內容進行。
  	+ 網站的架設(本實作是透過 [Flask](https://flask.palletsprojects.com/en/2.0.x/))。
  	+ 樹莓派能夠透通到internet([使用 ngrok 讓外網連接你的 API](https://ithelp.ithome.com.tw/articles/10197345))，提供URL 給外面(web/LINE)來連結使用。
  	+ LiNE 機器人(Bot) 的申請與設定可透過 [LINE Developers](https://developers.line.biz/zh-hant/docs/messaging-api/getting-started/)依步驟完成。

  + 軟硬體環境建置差不多時，就可以將各小功能的程式碼整合在一起，本實作相關程式碼放置於[python_code](https://github.com/molin-lin/IoT/tree/main/python_code) 資料夾內。
#### 成品外觀
 ![IoT.png](https://github.com/molin-lin/Image/blob/main/IoT.png "IoT.png" )
	
#### 執行啟用

   + 可透過以下QR Code 加入 LINE 機器人。
   	
        ![183xzqdi.png](https://github.com/molin-lin/Image/blob/main/183xzqdi.png "183xzqdi.png")

   + 如果開發過程中環頸經取得 ngrok token 並開啟終端機授權 `./ngrok authtoken[token]`，可直接下一步驟。
   + 建立 Chanel  `./ngrok http 5000` ，並取得URL (複製下來)
   + 透過Python 建立 Web Server (Port 必須跟  ngrok 一致)。 `python -m SimpleHTTPServer 5000`
   + 啟動 Web 程式。 `python3 practice_app.py`   (本實作的web server入口程式為 practice_app.py)
   + 將建立 ngrok channel 的 URL 在 LINE Developer->Message API->WebHook 中設定上去。(留意網頁LINE BOT call back 的路徑)
   + 接著就可以開始居家管理。
 


## 成果示範(影片長度 8分59秒)

<a href="http://www.youtube.com/watch?feature=player_embedded&v=1_ekMo24dV4
" target="_blank"><img src="http://img.youtube.com/vi/1_ekMo24dV4/0.jpg" 
alt="成果示範影片" width="240" height="180" border="10" /></a>

## 主要功能說明
   + 可透過執行紅外線感測，若有感應到移動物體，則執行拍照(照片依日期時間為檔名儲存)。 (Web/LINE)
   + 可遠端開啟攝影機。(Web)
   + 可遠端取得溫溼度資料。(Web/LINE)

## 改善方向與心得
   ***本實作可改善方向:***
   + 實作的鏡頭為固定不動，可結合步進馬達(PWM)來控制鏡頭方向，拍攝不同角度畫面。
   + 遠端操作環境 透過社群媒體 LINE Bot 遠比 Web 來得便利， 受限Message API目前只停留在訊息文字回覆，應可結合圖片或影音 API 增加實用性與有趣性。
   + 結合Google API 可以文字轉為語音，輸入之文字可透過樹莓派結合喇叭達到此目的。
   + 本實作目前可透過紅外線有感應時，透過鏡頭取得當時的影像紀錄，其最終是傳送圖片至 LINE Bot，進行影像辨識後回覆結果。
   + 可將現有功能製作成LINE Menu 取代關鍵字輸入。
   + 因設備將歸還學校，但將自行添購樹莓派等設備，持續改善，並不定期更新狀態。


   ***心得:***
   + 透過樹莓派進入IoT 的世界門檻不高，市面可找到很多終端套件來連接使用，端看自己想要達到甚麼樣的資料蒐集或遠端控制。而網路上也有很多前人寶貴經驗與程式撰寫分享，都是可以嘗試看看。
   + 但對第一次接觸IoT(樹莓派)+Python 來完成這個期末作業，真正困難的地方不是程式本身，而是在於沒有目標想法，也就沒有方向與進度，一旦確定後，接下來只是時間問題，因為會欲罷不能。
   

## 參考資料
[1]. [人體紅外線偵測](https://tutorials.webduino.io/zh-tw/docs/socket/sensor/pir.html "人體紅外線偵測") <br>
[2]. [教你如何使用Python成功串接Linebot(2020版)](https://ithelp.ithome.com.tw/articles/10229943"教你如何使用Python成功串接Linebot(2020版)") <br>
[3]. [Python+LINE Bot教學 6步驟快速上手LINE Bot機器人](https://www.learncodewithmike.com/2020/06/python-line-bot.html "Python+LINE Bot教學 6步驟快速上手LINE Bot機器人") <br>
[4]. [Messaging API 介紹](https://developers.line.biz/zh-hant/docs/messaging-api/overview/ "Messaging API 介紹") <br>
[5]. [樹莓派連接DHT22偵測溫濕度](https://ithelp.ithome.com.tw/articles/10238029 "樹莓派連接DHT22偵測溫濕度")<br>
[6]. [鏡頭套件問題](https://github.com/amymcgovern/pyparrot/issues/34#issuecomment-379557137) <br>
[7]. [API-picamera.camera Module](https://picamera.readthedocs.io/en/release-1.10/api_camera.html)

