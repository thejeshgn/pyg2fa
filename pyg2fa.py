#!/usr/bin/python
###############################################################################
# Repo: http://code.thejeshgn.com/pyg2fa
# Copyright (C) 2012 Thejesh GB <i@thejeshgn.com>
#
# 
#
# MIT License:
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
###############################################################################
import base64
import time
import math
import struct
import hashlib, hmac
import binascii

period = 30 #interval between two generated keys
length = 6  #length of OTP
b32 = {  "A" : 0, "B" : 1,"C" : 2, "D" : 3, "E" : 4, "F" : 5,  "G" : 6, "H" : 7,  "I" : 8, "J" : 9,  "K" : 10,     "L" : 11,  "M" : 12,     "N" : 13,  "O" : 14,     "P" : 15,  "Q" : 16,     "R" : 17,  "S" : 18,     "T" : 19,  "U" : 20,     "V" : 21,  "W" : 22,     "X" : 23,  "Y" : 24,     "Z" : 25,  "2" : 26,     "3" : 27,  "4" : 28,     "5" : 29,  "6" : 30,     "7" : 31 }


def decode(data):
	data 	= data.upper()
	n	= 0
	j	= 0
	binary = ""


	for char in data:
		n = n << 5
		n = n + b32[char]
		j = j + 5
		if j >= 8 :
			j = j - 8
			binary = binary+chr((n & (0xFF << j)) >> j);
	return binary

def timestamp():
	return int(round(time.time()/period))


def otp(key, time):
	bin_counter = struct.pack('!L', 0)+struct.pack('!L', time)
	# values = (time)
	# s = struct.Struct('!L')
	# packed_data = s.pack(values)
	# print 'Original values:', values
	# print 'Format string  :', s.format
	# print 'Uses           :', s.size, 'bytes'
	# print 'Packed Value   :', binascii.hexlify(packed_data)
	digest = hmac.new(key, bin_counter, hashlib.sha1)
	# print digest.hexdigest()
	result = str(truncate(digest.digest())).ljust(length, '0')
	return result

def truncate(hash):
	offset = ord(hash[19]) & 0xf;
	return (
	    ((ord(hash[offset+0]) & 0x7f) << 24 ) |
	    ((ord(hash[offset+1]) & 0xff) << 16 ) |
	    ((ord(hash[offset+2]) & 0xff) << 8 ) |
	    (ord(hash[offset+3]) & 0xff)
	) % pow(10, length)
	
 #Verifys a user inputted key against the current timestamp. Checks window
def validate(b32secretKey, userOTP, window = 4):
	timeStamp = timestamp()
	timeStampInInt = int(timeStamp)
	binarySeed = decode(b32secretKey)
	timestampRange = range(timeStampInInt-window, timeStampInInt+window)
	for ts in timestampRange:
		o = otp(binarySeed, ts)
		#print o
		if int(o) == int(userOTP):
			return True
	return False

def qrCodeURL(site, secretKey):
	return "http://chart.apis.google.com/chart?cht=qr&chs=300x300&chl=otpauth://totp/"+site+"?secret="+secretKey+"&chld=H|0"


#This is for testing only
def test():
	YOUR_SECRET_INITIAL_KEY = "KKK67SDNLXIOG65U"   # must be at least 16 base 32 characters, keep this secret
	print qrCodeURL("http://g2fa-example.com", YOUR_SECRET_INITIAL_KEY)
	userOTP = raw_input("Enter OTP: ")
	TIME_STAMP = timestamp()
	print validate(YOUR_SECRET_INITIAL_KEY, int(userOTP), 4)

