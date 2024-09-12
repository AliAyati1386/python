import subprocess
import sys
import random
import time
import os


def matrix_effect():  
    while True:
        
        # پاک کردن صفحه
        os.system('cls')
        
        
        # دریافت ابعاد ترمینال
        columns, rows = os.get_terminal_size()

        for _ in range(rows):
            # ایجاد یک خط تصادفی از 0 و 1
            line = ''.join(random.choice('YOU ARE HAKED ') for _ in range(columns))
            
            # چاپ خط
            print(line, end='')
        

        

if __name__ == "__main__":
    if sys.executable.endswith('pythonw.exe'):
        # اگر با pythonw اجرا شده، یک پنجره cmd جدید باز کن
        subprocess.Popen(['start', 'cmd', '/k', sys.executable, __file__], shell=True)
    else:
        try:
            matrix_effect()
        except KeyboardInterrupt:
            print("\nبرنامه متوقف شد.")
