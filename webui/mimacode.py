# 它使用 XOR 运算符对原始数据进行加密，然后再次使用 XOR 运算符对加密的数据进行解密。

def chuli(mima):
    #设置密码最大长度 多了截断，少了补齐
    MAX_TEST_NUM = 10
    # mima="12345678"
    if len(mima) > MAX_TEST_NUM:
        mima = mima[0:MAX_TEST_NUM]
    elif len(mima) < MAX_TEST_NUM:
        mima = mima + "0"*(MAX_TEST_NUM-len(mima))
    return mima

def jiami(mima):
    #设置密码最大长度 多了截断，少了补齐
    MAX_TEST_NUM = 10
    EncodeMachine = [0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x0A]
    # RawData = [0x68, 0x12, 0x34, 0x56, 0x78, 0x89, 0x0A, 0X0B, 0X0C, 0X0D]
    # mima="12345678"
    if len(mima) > MAX_TEST_NUM:
        mima = mima[0:MAX_TEST_NUM]
    elif len(mima) < MAX_TEST_NUM:
        mima = mima + "0"*(MAX_TEST_NUM-len(mima))

    print("原密码为:")
    print(mima)
    RawData = [0]*MAX_TEST_NUM
    for i in range(len(mima)):
        RawData[i]=mima[i]

    #转换为ASCII码
    print("原数据为:")
    for i in range(len(RawData)):
        RawData[i] = ord(RawData[i])
        print("0x%02x " % RawData[i], end='')
    
    EncodeData = [0]*MAX_TEST_NUM
    DecodeData = [0]*MAX_TEST_NUM

    print("\n加密数据为:")
    for i in range(MAX_TEST_NUM):
        EncodeData[i] = RawData[i]^EncodeMachine[i]
        print("0x%02x " % EncodeData[i], end='')

    # ... 其他代码 ...


    # # 将 EncodeData 写入到 txt 文件中
    # with open('encode_data.txt', 'w') as f:
    #     for item in EncodeData:
    #         f.write("%s " % item)

    tmpcode=""
    for item in EncodeData:
        tmpcode=tmpcode+str(item)+" "
    print(tmpcode)
    return tmpcode

def jiemi(mima):
    MAX_TEST_NUM = 10
    EncodeMachine = [0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x0A]
    DecodeData = [0]*MAX_TEST_NUM
    # 从 txt 文件中读取 EncodeData

    EncodeData = []
    #读入加密数据
    # with open('encode_data.txt', 'r') as f:
    #     lines = f.readlines()
    #     for line in lines:
    #         items = line.strip().split()
    #         for item in items:
    #             EncodeData.append(int(item))

    items = mima.strip().split()
    for item in items:
        EncodeData.append(int(item))

    # ... 其他代码 ...

    print("\n解密数据为:")
    for i in range(MAX_TEST_NUM):
        DecodeData[i] = EncodeData[i]^EncodeMachine[i]
        print("0x%02x " % DecodeData[i], end='')

    print("\n解密后密码为:")
    for i in range(MAX_TEST_NUM):
        print("%c" % DecodeData[i], end='')

    tmp = ""
    for i in range(MAX_TEST_NUM):
        tmp = tmp + chr(DecodeData[i])
    return tmp