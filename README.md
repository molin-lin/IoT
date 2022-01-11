# 居家環境遠端管理 - 以樹莓派實作
 
## 目的
  ### 透過樹苺派及Python架構一個原型(prototype)，可以透過Internet(Web/LINE)取得終端設備(eg.鏡頭、感測裝置、電器)之數據或控制。
  
## 硬體設備需求
   1. 樹莓派 * 1
   2. NOIR 鏡頭 * 1
   3. 七段顯示器 * 1
   4. 紅外線接收模組 * 1
   5. 麵包版/印刷電路板/Led/電阻/杜邦線 (視線路規劃而定)
   6. 簡易焊接設備(若不想把所有線路透過麵包版連接再一起)
## 軟體需求
   1. VNC viewer
   2. 

## 步驟


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

*install LINE Bot SDK
	>pip3 install line-bot-sdk


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

