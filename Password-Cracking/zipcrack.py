from zipfile import ZipFile 
import pyminizip
import itertools
from time import sleep
import os

from passwordcrack import PasswordCrack

# needs multiprocessing

class ZipCrack(PasswordCrack):
    """To use as a callable:
            crack_it = ZipCrack('protected.zip', 8)
            crack_it()

    If length of password is unknown, pass the callable into a range:
            crack_it = ZipCrack('protected.zip')
            for i in range(8,17):
                crack_it(i)

    Args:
        Name of zip archive (file)
        Length of password (pw_length)
    """

    processor = ZipFile
    #extraction = ZipFile.extractall

    def __init__(self, file=None, pw_length=None):
        super().__init__(file, pw_length)

    def __call__(self,length=None):
        """Making callable for quick use"""
        length = length or self.pw_length
        self.zippedContents(self.file)
        #self.brute_force(self.file, length, processor=ZipCrack.processor, extract=self.extract)
        self.brute_force(self.file, length, processor=ZipCrack.processor)

    def zippedContents(self, file):
        """Obtain a list of files within the archive"""
        zipped = ZipFile(file)  
        contents = zipped.namelist()
        zipped.close()
        self.contents = contents

    def reader(self, filelist):
        """Reads unzipped file to terminal"""
        for file in filelist:
            with open(file, 'r') as f:
                print(f"Filename: {file} \n")
                print(f.read(), '\n')

    def extract(zipfile_instance,pw):
        print(zipfile_instance.extractall(pwd=pw))
        return zipfile_instance.extractall(pwd=pw)

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
def test():
    crack=ZipCrack()
    TestZip.test_zip('bcb')

    crack.zippedContents('zippedTest.zip')
    crack.zipCrack('zippedTest.zip',3)

# testing callable instance
def iter_test():
    crack=ZipCrack('zippedTest.zip')
    TestZip.test_zip('bcb')
    sleep(2)
    for i in range(2,4):
        crack(i)
#tests()
iter_test()