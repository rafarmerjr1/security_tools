import itertools
from zipfile import ZipFile

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

    def brute_force(self, file, pw_length=6, processor=None, extract=None):
        """Attempt to brute force password"""
        found = False
        with processor(file) as target:
                # Use for Tests:
                for i in itertools.product(self.small_charlist, repeat=pw_length):
                # Use for real:
                #for i in itertools.product(self.charlist, repeat=pw_length):
                    pw = "".join(i)
                    pw = pw.encode('utf-8')
                    try:
                        #extract(target,pw)
                        target.extractall(pwd=pw)   # Need to find a way to make this agnostic to file type...  this is a zip specific call
                        found = True
                        break
                    except:
                        pass
                target.close()

        if found == False:
            print('Password not discovered on this iteration.')
        else:
            print(f'Password identified: {pw}\n')
            return self.reader(self.contents)