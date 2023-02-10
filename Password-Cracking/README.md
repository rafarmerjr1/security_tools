# Small Library of simple brute force tools 

Useful as a basis for zip, pdf, (sql in process) attempts.

## ZipCrack Class
Attempts to brute-force an encrypted zip file
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

## PDFCrack Class
Work in Progress

To-do:
- Implement some multiprocessing of threading
- implement wordlist functionality
    - Could split brute force method into two methods - one that creates a word list and one that uses it.
