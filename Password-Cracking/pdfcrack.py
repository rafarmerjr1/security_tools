import itertools
import pypdf



class PDFCrack(PasswordCrack):

    processor = 'pdf or whatever'

    def __init__(self, file=None, pw_length=None):
        super().__init__(file, pw_length)

    def __call__(self, pw_length=None):
        pass

    def test(self):
        print("test")
        print(self.file)



test_instance = PDFCrack('test.txt')
#test_instance.test()
