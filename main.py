import sys
import logging
import os
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from config.settings import LOG_FILE_PATH

# 1. ตรวจสอบและสร้างโฟลเดอร์สำหรับเก็บไฟล์ log
log_dir = os.path.dirname(LOG_FILE_PATH)
if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 2. กำหนดค่า logging ให้บันทึกข้อมูลลงในไฟล์และแสดงในคอนโซล
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE_PATH),  # บันทึกข้อมูลลงในไฟล์ app.log
        logging.StreamHandler(sys.stdout)    # แสดงข้อมูลบนหน้าจอคอนโซลด้วย
    ]
)

if __name__ == '__main__':
    # เพิ่ม log message สำหรับทดสอบ
    logging.info("Application started.")

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())