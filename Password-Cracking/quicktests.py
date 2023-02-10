import pyminizip
from time import sleep
import os

from passwordcrack import PasswordCrack, ZipCrack


class TestZip:

    def test_zip(pw):
        """Create a test zip file"""
        # password must be bytes:
        pw = pw.encode('utf-8') 
        with open("test.txt", "w") as testfile:
            testfile.write('HelloWorld')  
        pyminizip.compress('test.txt', None, './zippedTest.zip', pw, 0)
        os.remove("test.txt")

    
# Quick Test
# Replace with real unittests soon

if __name__ == '__main__':
    def test():
        TestZip.test_zip('bcb')
        crack=ZipCrack('zippedTest.zip',3)
        crack()

    # testing callable instance
    def iter_test():
        TestZip.test_zip('bcb')
        crack=ZipCrack('zippedTest.zip')
        sleep(1)
        for i in range(2,4):
            crack(i)
    test()
    #iter_test()