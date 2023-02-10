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
        """Generates list of characters to use against password
        Very Heavy.  Use with Caution."""
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
            return None
        else:
            return pw


class ZipCrack(PasswordCrack):
    """Attempts to brute-force an encrypted zip file
    Usage:
            'crack_it = ZipCrack('protected.zip', 8)
            crack_it()'
    If password length is unknown:
            'crack_it = ZipCrack('protected.zip')
            for i in range(8,17):
                crack_it(i)'
    Args:
        Name of zip archive (file)
        Length of password (pw_length)
    """
   
    def __init__(self, file=None, pw_length=None):
        super().__init__(file, pw_length)
        self.processor = ZipFile
        self.extractor = ZipFile(self.file).extractall

    def __call__(self,length=None):
        """Allows calling with file + pw_length or 
        length only, for iterating over possible pw_lengths
         """
        length = length or self.pw_length
        self.get_contents(self.file)
        self.try_brute(length)

    def get_contents(self, file):
        """Sets files within the archive to self.contents"""
        zipped = ZipFile(file)  
        contents = zipped.namelist()
        zipped.close()
        self.contents = contents

    def try_brute(self, length):
        """Main engine.  Attempts brute force and returns results."""
        pw = self.brute_force(self.file, length, self.processor, self.extractor)
        if pw:
            print(f'Password identified: {pw}\n')
            self.reader(self.contents)
            return pw
        else:
            print('Password not discovered on this iteration.')
            return None

    def reader(self, filelist):
        """Reads unzipped file to terminal"""
        for file in filelist:
            with open(file, 'r') as f:
                print(f"Filename: {file} \n")
                print(f.read(), '\n')

class PDFCrack(PasswordCrack):

    def __init__(self, file=None, pw_length=None):
        super().__init__(file, pw_length)
        self.processor = 'pdf or whatever'
        self.extractor = 'pdf extracting method'


    def __call__(self, pw_length=None):
        pw_length = pw_length or self.pw_length
        pass

    def pdf_info(self):
        pass

    def try_brute(self):
        pass

    def reader(self):
        pass
