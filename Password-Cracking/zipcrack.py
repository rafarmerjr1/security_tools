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
if __name__ == '__main__':
    def test():
        crack=ZipCrack()
        TestZip.test_zip('bcb')
        crack.zip_crack('zippedTest.zip',3)

    # testing callable instance
    def iter_test():
        crack=ZipCrack('zippedTest.zip')
        TestZip.test_zip('bcb')
        sleep(1)
        for i in range(2,4):
            crack(i)
    #test()
    iter_test()