import os
import numpy as np

IS_BENIGN_JS_HELPER = False      
MAX_L = 20000                   # Max number of characters in js code

src_prefix = ''
dst_prefix = ''
if IS_BENIGN_JS_HELPER:
  src_prefix = 'data/benign_js/'
  dst_prefix = 'data/benign_bin/'
else:
  src_prefix = 'data/malicious_js/'
  dst_prefix = 'data/malicious_bin/'

bin_f_name = 0
char_counter = 0
for warc_dir in os.listdir(src_prefix):
  print('.', end='', flush=True)
  for js in os.listdir(src_prefix + warc_dir):
    char_counter = 0
    src_f = open(src_prefix + warc_dir + '/' + js, 'rb')
    dst_f = open(dst_prefix + str(bin_f_name), 'w')
    while True:
      line = src_f.readline()
      if not line: 
        break
      for c in line:
        if char_counter < MAX_L:
          dst_f.write("{0:08b} ".format(c)) 
          char_counter += 1
    
    if char_counter < MAX_L:
      while char_counter < MAX_L:
        dst_f.write("{0:08b} ".format(0))
        char_counter += 1

    src_f.close()
    dst_f.close()
    bin_f_name += 1
