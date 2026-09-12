import time
import network
from network import WLAN, AP_IF
import socket
from micropython import const

from subsystems import chassis

m_chassis = chassis.Chassis()

# 請替換為你的 Wi-Fi 資訊
SSID = 'NCU BoltNut'
PASSWORD = 'ncuboltnut'

# 網頁前端原始碼 (HTML + CSS + JS)
html_page = html_page = """<!DOCTYPE html>
<html>
<head>
    <title>Pico W Debug Controller</title>
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <style>
        body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; background-color: #f0f0f0; user-select: none; -webkit-user-select: none; }
        .d-pad { display: grid; grid-template-columns: repeat(3, 80px); grid-template-rows: repeat(3, 80px); gap: 10px; margin-top: 30px; }
        button { font-size: 28px; border-radius: 15px; border: none; background-color: #007bff; color: white; cursor: pointer; touch-action: manipulation; }
        button:active { background-color: #0056b3; }
        .up { grid-column: 2; grid-row: 1; }
        .left { grid-column: 1; grid-row: 2; }
        .right { grid-column: 3; grid-row: 2; }
        .down { grid-column: 2; grid-row: 3; }
        #log { margin-top: 20px; font-weight: bold; color: #333; font-size: 20px; }
    </style>
</head>
<body>
    <h2>Debug 儀表板</h2>
    <div class="d-pad">
        <button class="up" 
            onmousedown="sendCommand('up')" onmouseup="sendCommand('stop')" onmouseleave="sendCommand('stop')"
            ontouchstart="sendCommand('up'); event.preventDefault();" ontouchend="sendCommand('stop'); event.preventDefault();">U</button>
        <button class="left" 
            onmousedown="sendCommand('left')" onmouseup="sendCommand('stop')" onmouseleave="sendCommand('stop')"
            ontouchstart="sendCommand('left'); event.preventDefault();" ontouchend="sendCommand('stop'); event.preventDefault();">L</button>
        <button class="right" 
            onmousedown="sendCommand('right')" onmouseup="sendCommand('stop')" onmouseleave="sendCommand('stop')"
            ontouchstart="sendCommand('right'); event.preventDefault();" ontouchend="sendCommand('stop'); event.preventDefault();">R</button>
        <button class="down" 
            onmousedown="sendCommand('down')" onmouseup="sendCommand('stop')" onmouseleave="sendCommand('stop')"
            ontouchstart="sendCommand('down'); event.preventDefault();" ontouchend="sendCommand('stop'); event.preventDefault();">D</button>
    </div>
    <div id="log">等待指令...</div>

    <script>
        let currentCommand = 'stop'; 

        function sendCommand(direction) {
            if (currentCommand === direction && direction !== 'stop') return; 
            currentCommand = direction;

            fetch(`/api/move?dir=${direction}`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('log').innerText = "當前狀態: " + data.direction.toUpperCase();
                })
                .catch(err => console.error(err));
        }
    </script>
</body>
</html>
"""

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    print('連線中', end='')
    while not wlan.isconnected():
        print('.', end='')
        time.sleep(1)
    
    ip = wlan.ifconfig()[0]
    print(f'\\nWi-Fi 連線成功！請在瀏覽器輸入: http://{ip}')
    return ip

def start_server():
    # 建立 Socket
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    
    # 允許重複使用 Port，避免重啟時卡住
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    print('伺服器監聽中...')

    while True:
        try:
            cl, addr = s.accept()
            print('Client 連線來自:', addr)
            
            # 接收 HTTP Request
            request: str = cl.recv(1024).decode('utf-8')
            if not request:
                cl.close()
                continue
                
            # 解析請求路徑 (例如: GET /api/move?dir=up HTTP/1.1)
            request_line = request.split('\\r\\n')[0]
            path = request_line.split(' ')[1]

            # 路由設計
            if path == '/':
                # 回傳主網頁
                response_header = 'HTTP/1.1 200 OK\\r\\nContent-Type: text/html\\r\\n\\r\\n'
                cl.send(response_header.encode('utf-8'))
                cl.send(html_page.encode('utf-8'))
                
            elif path.startswith('/api/move'):
                # 處理 API 請求
                direction = "stop"
                if "dir=up" in path: direction = "up"
                elif "dir=down" in path: direction = "down"
                elif "dir=left" in path: direction = "left"
                elif "dir=right" in path: direction = "right"
                
                print(f"[debug] 收到移動指令: {direction}")
                # control chassis based on `direction`
                if direction == "up":
                    m_chassis.drive(1, 0)  # 前進
                elif direction == "down":
                    m_chassis.drive(-1, 0)  # 後退
                elif direction == "left":
                    m_chassis.drive(0, 1)  # 左轉
                elif direction == "right":
                    m_chassis.drive(0, -1)  # 右轉
                else:
                    m_chassis.drive(0, 0)  # 停止
                
                # 回傳 JSON
                response_body = f'{{"status": "success", "direction": "{direction}"}}'
                response_header = 'HTTP/1.1 200 OK\\r\\nContent-Type: application/json\\r\\n\\r\\n'
                cl.send(response_header.encode('utf-8'))
                cl.send(response_body.encode('utf-8'))
                
            else:
                # 404 Not Found
                response_header = 'HTTP/1.1 404 Not Found\\r\\nContent-Type: text/plain\\r\\n\\r\\n'
                cl.send(response_header.encode('utf-8'))
                cl.send(b'404 Not Found')

            cl.close()
            
        except Exception as e:
            print("發生錯誤:", e)
            cl.close()

# 執行程式
try:
    connect_wifi()
    start_server()
except KeyboardInterrupt:
    print("Server interrupted by user")
