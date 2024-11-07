import sys
import os

# Hàm mã hóa dữ liệu
def process_data(input_bytes, key):
    key_bytes = key.encode('utf-8')
    return bytearray([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(input_bytes)])

# Hàm xử lý các tệp trong thư mục
def process_all_files(key):
    for filename in os.listdir('.'):
        if os.path.isfile(filename):
            print(f'Processing file: {filename}')

            # Đọc dữ liệu từ tệp
            with open(filename, 'rb') as f:
                input_data = f.read()

            # Mã hóa dữ liệu
            result_data = process_data(input_data, key)

            # Thay đổi phần mở rộng tên tệp thành .kzb
            encoded_filename = filename + '.kzb'

            # Lưu tệp đã mã hóa với tên mới
            with open(encoded_filename, 'wb') as f:
                f.write(result_data)

            print(f'File has been encoded and saved as: {encoded_filename}')

def main():
    if len(sys.argv) != 2:
        print('Usage: python script.py <key>')
        return

    key = sys.argv[1]
    process_all_files(key)

if __name__ == '__main__':
    main()
