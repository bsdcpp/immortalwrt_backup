import base64
import urllib.parse
import requests

def decode_base64_with_padding(data):
    # 计算缺少的 "=" 数量，并进行填充
    missing_padding = len(data) % 4
    if missing_padding:
        data += '=' * (4 - missing_padding)
    data = data.replace('-', '+').replace('_', '/')
    return base64.b64decode(data)

# Step 2: 处理每行 SSR 链接
def ssr_to_ss(ssr_link):
    # 移除 "ssr://" 前缀
    ssr_link = ssr_link.replace('ssr://', '')
    decoded_ssr = decode_base64_with_padding(ssr_link).decode('utf-8')
    #print(ssr_link, decoded_ssr)

    # 提取服务器、端口、加密方式和密码
    parts = decoded_ssr.rsplit(":", 5)
    server = parts[0]
    port = parts[1]
    encryption = parts[3]

    # 提取密码并进行 Base64 解码
    query_params = urllib.parse.parse_qs(parts[5])
    password_base64 = parts[5].split("/")[0]
    password = decode_base64_with_padding(password_base64).decode('utf-8')
    remarks = urllib.parse.quote(decode_base64_with_padding(query_params['remarks'][0]).decode('utf-8'))

    # 将提取的信息转换为 SS 链接
    ss_info = f"{encryption}:{password}"
    ss_base64 = base64.b64encode(ss_info.encode('utf-8')).decode('utf-8')
    ss_link = f"ss://{ss_base64}@{server}:{port}#{remarks}"

    return ss_link


if __name__ == "__main__":
    # Step 1: 从URL下载base64文件并解码
    url = "http://192.168.2.248/clash/ssr.txt"
    response = requests.get(url)
    base64_data = response.text

    # 将 Base64 解码并按行分割
    decoded_data = decode_base64_with_padding(base64_data).decode('utf-8')
    ssr_links = decoded_data.splitlines()

    # 转换所有 SSR 链接为 SS 链接
    ss_links = [ssr_to_ss(link) for link in ssr_links]

    # Step 3: 将转换后的 SS 链接编码为 Base64 并输出
    final_output = "\n".join(ss_links)
    final_base64 = base64.b64encode(final_output.encode('utf-8')).decode('utf-8')

    # 将结果写入文件
    with open('ss.txt', 'w') as f:
        f.write(final_base64)

    print("转换完成，结果已保存为 ss.txt")
