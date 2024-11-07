import sys
import os

# Hàm mã hóa dữ liệu
def process_data(input_bytes, key):
    key_bytes = key.encode('utf-8')
    return bytearray([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(input_bytes)])

# Hàm mã hóa tên tệp
def encode_filename(filename, key):
    key_bytes = key.encode('utf-8')
    encoded_name = bytearray([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(filename.encode('utf-8'))])
    return encoded_name.decode('latin1', errors='ignore')

# Hàm xử lý tất cả các tệp trong thư mục hiện tại
def process_all_files(key):
    current_directory = os.getcwd()
    for filename in os.listdir(current_directory):
        file_path = os.path.join(current_directory, filename)
        
        if os.path.isfile(file_path):
            print(f'Processing file: {filename}')
            
            with open(file_path, 'rb') as f:
                input_data = f.read()
            
            result_data = process_data(input_data, key)
            
            # Mã hóa tên tệp đầu ra và thay đổi phần mở rộng thành .kzb
            encoded_filename = encode_filename(filename, key) + '.kzb'
            
            with open(encoded_filename, 'wb') as f:
                f.write(result_data)
            
            print(f'File has been encoded and saved as: {encoded_filename}')

# Hàm chính để bắt đầu xử lý
def main():
    if len(sys.argv) != 2:
        print('Usage: python script.py <key>')
        return
    
    key = sys.argv[1]
    process_all_files(key)

if __name__ == '__main__':
    main()
