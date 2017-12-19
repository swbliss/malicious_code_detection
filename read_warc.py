import builtins
import os
from hanzo import warctools 


IS_BENIGN_JS_EXTRACTOR = False 
warc_dir = '/home/swjung/cs548/heritrix-3.1.1/jobs/malicious/20161115041828/warcs/'


for warc_f in os.listdir(warc_dir):
  
  if warc_f[-4:] == 'open':
    continue

  print('\n########################################################')
  print('#############' + warc_f + '##########')
  print('########################################################')
  
  warc_path = warc_dir + warc_f
  warc_stream = warctools.WarcRecord.open_archive(warc_path)

  js_count = 0
  is_res = False
  is_js = False

  if IS_BENIGN_JS_EXTRACTOR:
    js_dir = 'data/benign_js/' + warc_f[:-8] + '/'
  else:
    js_dir = 'data/malicious_js/' + warc_f[:-8] + '/'

  if not os.path.exists(js_dir):
    os.makedirs(js_dir)

  for record in warc_stream:
    print('.', end='', flush=True)
    for (h,v) in record.headers:
      if h.decode('utf-8') == 'WARC-Type' and v.decode('utf-8') == 'response':
        is_res = True
      if h.decode('utf-8') == 'WARC-Target-URI' and\
          v.decode('utf-8')[-3:] == '.js':
        is_js = True

    if is_res and is_js:
      content = record.content[1]
      if content[9:12] == b'200':
        f = open(js_dir + str(js_count), 'wb')
        f.write(b''.join(content.split(b'\r\n\r\n')[1:]))
        f.close()
        js_count += 1

    is_res = False
    is_js = False

  os.remove(warc_path)
