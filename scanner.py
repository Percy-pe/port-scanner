import socket
from concurrent.futures import ThreadPoolExecutor

def scan_port(port, host):
    #核心扫描函数：尝试通过 TCP 连接目标主机的特定端口。
    #返回：如果开放则返回提示字符串，关闭则返回 None，报错则返回错误信息。
    try:
        # 创建 TCP Socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         # 设置超时时间为 0.5 秒，防止在未响应的端口上卡死
        s.settimeout(0.5)
        # connect_ex 尝试连接，成功返回 0，失败返回错误码
        result = s.connect_ex((host, port))
        s.close()
        
        if result == 0:
            return f"[+] 端口 {port} 开放"
        else:
            # 端口未开放（如错误码 10035，表示非阻塞超时），直接返回 None 跳过打印
            return None
    except Exception as e:
        # 捕获系统底层的突发错误（如并发过高导致资源耗尽），防止整个程序崩溃
        return f"[!] 端口 {port} 崩溃: {str(e)}"

def main():
    host = input("输入目标IP：")
    ports = input("输入端口范围：")
    # 解析用户输入的端口范围（例如 1-1000 切割成 start=1, end=1000）
    start, end = ports.split("-")
    start = int(start)
    end = int(end)
    
    print(f"开始扫描 {host} 的 {start} 到 {end} 端口...\n")
    
    # 生成所有的端口任务列表
    port_list = list(range(start, end + 1))
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        # map 会确保每个任务的结果都被收集回来
        # 这里用了 lambda 是因为 map 传多个参数比较麻烦，先固定 host
        results = executor.map(lambda p: scan_port(p, host), port_list)
        
        # 把结果打印出来
        for res in results:
            # 过滤掉返回 None（未开放）的端口，只打印有价值的输出
            if res is not None:
                print(res)
            
    print("\n扫描结束！")

if __name__ == "__main__":
    main()
