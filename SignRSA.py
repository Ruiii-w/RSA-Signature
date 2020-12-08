import random
import hashlib
letterslen = [0]    # 每个字符转成ASCII码的十进制数的长度

# 切割messageIntStr ，使每部分都小于n 且切割单元长由letterslen里的元素累加获得
def splitMessage(messageIntStr, nStr):
    message = ''
    messageList = []
    mlen = len(letterslen)
    pos1 = letterslen[0]
    pos2 = letterslen[0]
    # print(letterslen)
    for i in range(mlen):
        # pos2 += letterslen[i + 1]
        if len(message) + letterslen[i] >= len(nStr):

            messageList.append(message)
            message = ''

        pos2 += letterslen[i]
        # print('pos1', pos1)
        # print('pos2', pos2)
        # print('messageIntStr', messageIntStr[pos1:pos2])
        message += messageIntStr[pos1:pos2]
        pos1 = pos2
    if message != '':
        # 最后一个分组，
        # 若最后一组分组长度满足len(message) + letterslen[i] >= len(nStr)
        # 则 message = ‘’ 不需加进messageList中
        messageList.append(message)
    return messageList


'''明文转换：字母串转数字'''
def str2int(text):
    lis = list(text)
    num = ''
    # print(lis)
    for e in lis:
        hexstr = str(ord(e))
        # print('hex:',hexstr)
        letterslen.append(len(hexstr))
        num += hexstr
    # print(letterslen)
    return int(num)


''' 明文复原：整型转字符串'''
def int2str(num):
    hexstr = str(num)
    # print(hexstr)
    # mlen = len(letterslen)
    mes = ''
    pos1 = letterslen[0]
    pos2 = letterslen[0]
    # print(letterslen)
    while 1:
        if len(letterslen) >= 2:
            pos2 += letterslen[1]

        if hexstr[pos1:pos2] != '':
            letterslen.pop(1)
            # i -= 1  # 后面的元素往前移  索引不动

            # print('pos1', pos1)
            # print('pos2', pos2)
            # print('hexSubstr', hexstr[pos1:pos2])
            hexSub = int(hexstr[pos1:pos2])
            # if hexSub != '':
            mes += chr(hexSub)   # 将数字字符串先转成int类型  chr通过ASCII码将其转为字符
            pos1 = pos2
        else:
            return mes

    # return mes


def fast_power(base, power, n):
    result = 1
    tmp = base
    while power > 0:
        if power&1 == 1:
            result = (result * tmp) % n
        tmp = (tmp * tmp) % n
        power = power>>1
    return result


'''判断n是否为素数'''
def rabin_miller(n,iter_num):
    if n == 2:
        return True
    # if n is even or less than 2, then n is not a prime
    if n & 1 == 0 or n < 2:
        return False
    # n-1 = (2^s)m
    m,s = n - 1,0
    while m & 1==0:
        m = m >> 1
        s += 1
    # M-R test
    for _ in range(iter_num):
        b = fast_power(random.randint(2,n-1), m, n)
        if b==1 or b== n-1:
            continue
        for __ in range(s-1):
            b = fast_power(b, 2, n)
            if b == n-1:
                break
        else:
            return False
    return True


''' 返回两个大素数p和q'''
''' start : 数据下限
    stop  : 数据上限    
'''
def getKeyPrime(start,stop):

    num1 = random.randint(start,stop - 1)
    num2 = random.randint(start,stop - 1)
    i = 0
    while not rabin_miller(num1,10):
        num1 = random.randint(start, stop - 1)
        # print(num1)
        # print(i)
        i += 1
    # print(num1, '-----1 yes')
    while not rabin_miller(num2,10):
        num2 = random.randint(start, stop - 1)
    # print(num2, '-----2 yes')
    return num1,num2


'''判断两数是否互质'''
def gcd(a, b):
    if a < b:
        return gcd(b, a)
    while a % b != 0:
        temp = b
        b = a % b
        a = temp
    return b


'''求a模b的逆元  即'''
def in_gcd(a, b):
    if b == 0:
        return 1, 0
    else:
        k = a // b
        remainder = a % b
        x1, y1 = in_gcd(b, remainder)
        x, y = y1, x1 - k * y1
    return x, y


# c = a**b mod n
''' RSA加密 '''
def encrypt(a,b,n):
    y = 1
    while (1):
        if b == 0:
            return y
        while b > 0 and b % 2 == 0:
            a = (a * a) % n
            b = b / 2
        b = b - 1
        y = (a * y) % n


''' RSA解密'''
def decrypt(a,b,n):
    y = 1
    while (1):
        if b == 0:
            return y
        while b > 0 and b % 2 == 0:
            a = (a * a) % n
            b = b / 2
        b = b - 1
        y = (a * y) % n

# import sys

def main():
    key_bit = 17  # 密钥位数
    message = 'Time goes by so fast, people go in and out of your life. You must never miss the opportunity to tell these people how much they mean to you.' # 明文
    # message = SHA1plain
    print('明文message:', message)
    messageDigest = hashlib.sha1(message.encode("utf-8")).hexdigest() # hash算法 获得摘要

    print('信息摘要:',messageDigest)
    messageDigest_to_Int = str2int(messageDigest)
    # messageInt = str2int(message)
    # print(messageInt)

    p,q = getKeyPrime(2**(key_bit-1),2**key_bit)
    # print('p is',p,'\n')
    # print('q is',q,'\n')
    n = p * q
    print('RSA公钥n:', n)
    fi_n = (p - 1) * (q - 1)

    e = random.randint(0, fi_n - 1)  # 加密公钥
    while gcd(e, fi_n) != 1:
        e = random.randint(0, fi_n - 1)

    print('RSA公钥e:', e)
    x, y = in_gcd(e, fi_n)
    d = x % fi_n  # 私钥

    # print('RSA私钥d:', d)
    messageDigest_dec = ''
    '''*************************** if m > n  需要分组   ***************************'''
    if messageDigest_to_Int > n:
        i = 0

        messageIntStr = str(messageDigest_to_Int)
        # print("messageIntStr:", messageIntStr)
        nStr = str(n)
        # print('n to str is:', nStr)
        messageList = splitMessage(messageIntStr, nStr)
        # print('messageList is', messageList)
        message2 = ''
        cipher = ''
        for mesStr in messageList:
            mes = int(mesStr)
            # print('the message is encrypting is:', mes)
            cipher_tmp = encrypt(mes, d, n)  # RSA签名私钥加密
            # print('encrypt code is ', cipher_tmp)
            cipher += str(cipher_tmp)

            '''*****************************解密*****************************'''
            messageInt = decrypt(cipher_tmp, e, n)  # RSA签名公钥解密
            # print('decrypt code (int) is ', messageInt)
            message2 += int2str(messageInt)
            '''*****************************解密*****************************'''

        # print('encrypt code:', cipher)  # 密文
        # print('decrypt code:', message2)  # 解密后的明文
        messageDigest_dec = message2
    # *************************** if m < n  不需要分组   ***************************'''
    else:
        cipher = encrypt(messageDigest_to_Int, d, n)  # RSA签名私钥加密
        # print('encrypt code:', cipher)

        '''*****************************解密*****************************'''
        messageInt = decrypt(cipher, e, n)  # RSA签名公钥解密
        message3 = int2str(messageInt)
        # print('decrypt code:', message3) # 解密后的明文
        messageDigest_dec = message3
        '''*****************************解密*****************************'''

    print('摘要的数字签名:', cipher)

    print('解密后的摘要:', messageDigest_dec)

    '''接收方Hash加密获取摘要前，可以修改明文， 模拟假明文'''
    # message = ''.join(random.sample(message,len(message)))
    # print('\n随机生成的message:',message)
    '''接收方Hash加密获取摘要前，可以修改明文， 模拟假明文'''

    messageDigest_rec = hashlib.sha1(message.encode("utf-8")).hexdigest()  # hash算法 获得摘要

    print('接收方的加密摘要:', messageDigest_rec)
    print('进行对比认证')
    if messageDigest_dec == messageDigest_rec:
        print('Correct message')
    else:
        print('Fake message')
if __name__ == '__main__':
    main()