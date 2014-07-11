import ctypes
import sys

def zerome_string(string):
    '''Remove the contents of a string object from memory.
    Derived from: http://web.archive.org/web/20100929111257/http://www.codexon.com/posts/clearing-passwords-in-memory-with-python
    '''
    def header_size():
        temp = "finding offset"
        raw_temp = ctypes.string_at(id(temp), sys.getsizeof(temp))
        return raw_temp.find(temp)
    def location(s):
        return id(s) + header_size()
    def size(s):
        return sys.getsizeof(s) - header_size()

    ctypes.memset(location(string), 0, size(string))

def zerome_unicode_string(string):
    def header_size():
        temp = "finding offset"
        raw_temp = ctypes.string_at(id(temp), sys.getsizeof(temp))
        print '\nraw_temp', repr(raw_temp)
        return raw_temp.find(temp)
    def location(s):
        return id(s) + header_size()
    def size(s):
        return sys.getsizeof(s) - header_size()

    ctypes.memset(location(string), 0, size(string))

    print 'after zerome', repr(string)
