from zipfile import ZipFile 
import pyminizip
import itertools

# needs multiprocessing

class ZipCrack:
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

    def __init__(self, file=None, pw_length=None):
        self.charlist = [chr for chr in self.chr_list_creator()]
        self.small_charlist = [ 'a', 'b', 'c']  # for testing
        self.contents = []
        self.file = file
        self.pw_length = pw_length

    def __call__(self,length=None):
        """Making callable for quick use"""
        length = length or self.pw_length
        self.zippedContents(self.file)
        self.zipCrack(self.file, length)

    def chr_list_creator(self, start=32, end=126):
        """Generates list of characters to use against password"""
        for i in range(start,end):
            yield chr(i)

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

    def zipCrack(self, file, pw_length=6):
        """Attempt to brute force password"""
        found = False
        processor = ZipFile
        with ZipFile(file) as target:
                # Use for Tests:
                for i in itertools.product(self.small_charlist, repeat=pw_length):
                # Use for real:
                #for i in itertools.product(self.small_charlist, repeat=pw_length):
                    pw = "".join(i)
                    pw = pw.encode('utf-8')
                    try:
                        target.extractall(pwd=pw)
                        found = True
                        break
                    except:
                        pass
                target.close()

        if found == False:
            print('Password not discovered.')
        else:
            print(f'Password identified: {pw}\n')
            return self.reader(self.contents)

class TestZip:

    def test_zip(pw):
        """Create a test zip file"""
        # password must be bytes:
        pw = pw.encode('utf-8') 
        with open("test.txt", "w") as testfile:
            testfile.write('HelloWorld')  
        pyminizip.compress('test.txt', None, './zippedTest.zip', pw, 0)
    
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
    for i in range(2,4):
        crack(i)
#tests()
iter_test()