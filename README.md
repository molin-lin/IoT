# 居家環境遠端管理 - 以樹莓派實作
 
## 目的
   透過樹苺派及Python架構一個原型(prototype)，可以透過Internet(Web/LINE)取得終端設備(eg.鏡頭、感測裝置、電器)之數據或控制。
  
## 硬體設備需求
   1. 樹莓派 * 1
   2. [NOIR 鏡頭](https://safe.menlosecurity.com/https://www.uctronics.com/raspberry-pi-noir-camera-board-w-cs-mount-lens-compatible-with-official-module.html) * 1
   3. [DHT22](https://www.raspberrypi.com.tw/23140/dht22-temperature-and-humidity-sensor/) 溫溼度感測模組 * 1
   4. 七段顯示器 * 1 (純為測試與噱頭用，可有可無)
   5. 紅外線接收模組 * 1
   6. 麵包版/印刷電路板/Led/電阻/杜邦線 (視線路規劃而定)
   7. 簡易焊接設備(若不想把所有線路透過麵包版連接再一起)
   8. 紙箱或薄木板(固定相關設備，方便移動及避免電路鬆脫)
## 軟體及環境需求
   1. VNC viewer
## 注意事項

   1. 為確保系統Python程式除錯過程順利，會先完成電路接線，並透過簡易程式確認GPIO 各項接點控制led，方便確認能夠正常運作，才進行Python 程式撰寫。
   2. 鏡頭及紅外線體感偵測器(PIR)怕靜電，接線過程中要確定完成去除靜電。
   3. PIR接線前要確認三根接腳哪支接腳是接地(GND)，可以把白色遮罩蓋拿起來確認。為了實作過程方便測試，可調整紅外線偵測器的靈敏度(SX)調高, 延遲時間(TX)調低。(順時針方向都是調高)
   4. 
## 過程及步驟

### 步驟流程如下圖，前提是樹莓派基本環境已經ready且有python compiler，整個系統架構需要完成的就是.....

  1. 網站的架設(eg.Flask)。
  2. 樹莓派能夠透通到internet(eg.ngrok)，提供URL 給外面(web/LINE)來連結使用。
  3. LiNE 機器人(Bot) 的申請與設定


*. Setup Flask (網站開方框架函式庫)
*. setup camera for python 
   >Install command - pip install opencv-python


*. Create web_app.py
*. python3 web_app.py  


*. Setup ngrok

	a. https://dashboard.ngrok.com/get-started/setup

*. Setup environment
	b. get authtoken
	c. ./ngrok authtoken [token]
	d. ./ngrok http 5000

*安裝 LINE Bot SDK
  執行指令：`pip3 install line-bot-sdk`


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
[1]. https://tutorials.webduino.io/zh-tw/docs/socket/sensor/pir.html <br>
[2]. https://ithelp.ithome.com.tw/articles/10229943 <br>
[3]. https://developers.line.biz/zh-hant/docs/messaging-api/overview/ <br>

