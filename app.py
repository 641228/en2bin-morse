from flask import Flask, request, jsonify, render_template_string
import yaml

app = Flask(__name__)

# 读取配置
with open("config.yml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# 升级摩斯码表：支持字母、数字、常用标点
MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    ' ': '/',
    ',': '--..--', '.': '.-.-.-', '?': '..--..', "'": '.----.', '!': '-.-.--',
    '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...', ':': '---...',
    ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-',
    '"': '.-..-.', '$': '...-..-', '@': '.--.-.'
}

# 升级二进制算法
def to_binary(text: str, bits: int = 8) -> str:
    text = text.strip()
    if not text:
        return ""
    return ' '.join([
        format(ord(char), '0{}b'.format(bits))
        for char in text
    ])

# 升级摩斯算法
def to_morse(text: str) -> str:
    text = text.strip().upper()
    result = []
    for char in text:
        if char in MORSE_CODE:
            result.append(MORSE_CODE[char])
    return ' '.join(result)

# 首页（全中文前端）
@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>英文 → 二进制 & 摩斯密码</title>
    <style>
        *{box-sizing:border-box;font-family: "Microsoft YaHei", sans-serif}
        body{max-width:900px;margin:3rem auto;padding:0 1rem;line-height:1.6}
        textarea{width:100%;height:140px;padding:1rem;font-size:1rem;border-radius:6px;border:1px solid #ddd}
        button{padding:.8rem 2.5rem;background:#007bff;color:#fff;border:none;border-radius:6px;cursor:pointer;margin:1rem 0;font-size:1rem}
        .result{background:#f8f9fa;padding:1.2rem;border-radius:6px;white-space:pre-wrap;font-family:Consolas,monospace}
        h1{color:#222}
    </style>
</head>
<body>
    <h1>英文 → 二进制 & 摩斯密码 转换工具</h1>
    <textarea id="inputText" placeholder="请输入英文语句..."></textarea>
    <br/>
    <button onclick="doConvert()">开始转换</button>
    <div class="result" id="resultArea"></div>

    <script>
        async function doConvert() {
            const text = document.getElementById('inputText').value.trim();
            if (!text) {
                alert('请输入内容');
                return;
            }
            const resp = await fetch('/api/convert', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text })
            });
            const data = await resp.json();
            document.getElementById('resultArea').innerText =
                `输入原文：${data.input}\n\n` +
                `8位二进制：\n${data.binary_8bit}\n\n` +
                `摩斯密码：\n${data.morse}`;
        }
    </script>
</body>
</html>
    ''')

# API 接口
@app.route('/api/convert', methods=['POST'])
def api_convert():
    data = request.get_json()
    text = data.get('text', '').strip()
    if not text:
        return jsonify({"error": "文本不能为空"}), 400

    return jsonify({
        "input": text,
        "binary_8bit": to_binary(text, 8),
        "morse": to_morse(text)
    })

if __name__ == '__main__':
    c = config['flask']
    app.run(host=c['host'], port=c['port'], debug=c['debug'])