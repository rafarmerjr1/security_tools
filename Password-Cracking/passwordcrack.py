from zipfile import ZipFile 
import pyminizip
import itertools
from time import sleep
import os
import pypdf

"""
Class created to play around with attacking zip and pdf files.  
Parent class should be capable of accepting filetype-specific methods for opening and extracting
files during brute force operation.
Specifically - processor and extractor will vary based on what kind of file is being opened. 
"""


class PasswordCrack:
    def __init__(self, file=None, pw_length=None):
        self.charlist = [chr for chr in self.chr_list_creator()]
        self.medium_charlist = [ 'a', 'b', 'c', 'd', 'e', '1', '2', '3', '4', '5', '6' ]  # for testing
        self.small_charlist = [ 'a', 'b', 'c'] # for testing
        self.file = file
        self.pw_length = pw_length

    def __call__(self):
        raise NotImplementedError

    def chr_list_creator(self, start=32, end=126):
        """Generates list of characters to use against password"""
        for i in range(start,end):
            yield chr(i)

    def brute_force(self, file, pw_length=6, processor=None, extractor=None):
        """Attempt to brute force password
        Args:
            file and password length
            processor = filetype-specific method of opening as determined by this method's caller
            extractor = filetype-specific method of extracting content as determined by this method's caller
        """
        found = False
        with processor(file) as target:
                for i in itertools.product(self.small_charlist, repeat=pw_length):
                #for i in itertools.product(self.charlist, repeat=pw_length):
                    pw = "".join(i)
                    pw = pw.encode('utf-8')
                    try:
                        extractor(pwd=pw)
                        found = True
                        break
                    except:
                        pass
        if found == False:
            print('Password not discovered on this iteration.')
        else:
            print(f'Password identified: {pw}\n')
            return self.reader(self.contents)


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
    extraction = ZipFile.extractall

    def __init__(self, file=None, pw_length=None):
        super().__init__(file, pw_length)

    def __call__(self,length=None):
        """Making callable for quick use during iteration of pw_lengths"""
        length = length or self.pw_length
        self.zippedContents(self.file)
        extractor = ZipCrack.processor(self.file).extractall
        self.brute_force(self.file, length, processor=ZipCrack.processor, extractor=extractor)

    def zippedContents(self, file):
        """Obtain a list of files within the archive"""
        zipped = ZipFile(file)  
        contents = zipped.namelist()
        zipped.close()
        self.contents = contents

    def zip_crack(self, file, length):
        """Allows calling decryption attack directly with filename and pw length"""
        self.file = file
        self.zippedContents(file)
        extract = ZipCrack.processor(self.file).extractall
        self.brute_force(self.file, length, processor=ZipCrack.processor, extract=extract)

    def reader(self, filelist):
        """Reads unzipped file to terminal"""
        for file in filelist:
            with open(file, 'r') as f:
                print(f"Filename: {file} \n")
                print(f.read(), '\n')

    #def extract(zipfile_instance,pw):
    #    print(zipfile_instance.extractall(pwd=pw))
    #    return zipfile_instance.extractall(pwd=pw)



class PDFCrack(PasswordCrack):
    processor = 'pdf or whatever'

    def __init__(self, file=None, pw_length=None):
        super().__init__(file, pw_length)

    def __call__(self, pw_length=None):
        pw_length = pw_length or self.pw_length
        pass

    def pdf_info(self):
        pass

    def pdf_crack(self):
        pass

    def reader(self):
        pass
