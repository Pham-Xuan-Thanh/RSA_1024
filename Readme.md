# Run 
Chạy câu lệnh sau:
```
$ python3.8 RSA_1024.py todo arguments
```
* Trong đó:
    * todo :
        * 'gen' : tạo ra các PublicKey and PrivateKey
            * Argument : Là _số lượng bit_ cần đề tạo ra Key
        * 'enc' : Mã hóa thông tin thành mật mã
            *Argument : 1. e 2. n 
        * 'dec' : Giải mã mật mã được mã hóa
            *Argument : 1. d 2. n
        * 'fdec' : Giải mã mật mã nhanh hơn tối ưu hơn phương pháp trên
            *Argument : 1. d 2. n 3. p 4. q
# Example
```
$ pyhthon3.8 RSA_1024 enc 12354 98754646
```
