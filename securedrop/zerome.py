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
    location = id(string) + header_size()
    size = sys.getsizeof(string) - header_size()

    ctypes.memset(location, 0, size)


class _PyUnicodeObjectStruct(ctypes.Structure):
    '''Include/object.h:77
    #define PyObject_HEAD                   \
        _PyObject_HEAD_EXTRA                \
        Py_ssize_t ob_refcnt;               \
        struct _typeobject *ob_type;

    Include/unicodeobject.h:413
    typedef struct {
        PyObject_HEAD
        Py_ssize_t length;          /* Length of raw Unicode data in buffer */
        Py_UNICODE *str;            /* Raw Unicode buffer */
        long hash;                  /* Hash value; -1 if not set */
        PyObject *defenc;           /* (Default) Encoded version as Python
                                    string, or NULL; this is used for
                                    implementing the buffer protocol */
    } PyUnicodeObject;
    '''
    _fields_ = [
        ('ob_refcnt', ctypes.c_size_t),
        ('ob_type', ctypes.c_void_p),
        ('length', ctypes.c_size_t),
        ('str', ctypes.POINTER(ctypes.c_wchar)),
        ('hash', ctypes.c_long),
        ('defenc', ctypes.c_void_p)
    ]

def _unicode_bytes_per_char():
    '''Python can be compiled for either "thin" or "wide" unicode support.
    A thin build uses two bytes to store unicode characters, while the
    wide build uses four. Not all unicode characters can be represented
    in two byes, so trying to create a character from a high unicode
    value tells us if we have a wide or thin build.
    https://docs.python.org/2/library/functions.html#unichr
    '''
    try:
        unichr(0x10000)
        return 4 # wide build -> UCS4 -> 4 bytes
    except ValueError:
        return 2 # thin build -> UCS2 -> 2 bytes

def zerome_unicode_string(string):
    string_pointer = ctypes.c_void_p(id(string))
    c_type = ctypes.POINTER(_PyUnicodeObjectStruct)
    string_struct = ctypes.cast(string_pointer, c_type).contents
    raw_string_size = string_struct.length * _unicode_bytes_per_char()

    ctypes.memset(string_struct.str, 0, raw_string_size)
