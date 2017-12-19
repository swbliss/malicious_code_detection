import os


IS_BENIGN_JS_COUNTER = True

dir_prefix = ''
if IS_BENIGN_JS_COUNTER:
  dir_prefix = 'data/benign_js/'
else:
  dir_prefix = 'data/malicious_js/'
js_count = 0
avg_l = 0
avg_count = 0
max_l = 0
max_path = ''

for warc_dir in os.listdir(dir_prefix):
  js_count += len(os.listdir(dir_prefix + warc_dir)) 
  for js in os.listdir(dir_prefix + warc_dir):
    f = open(dir_prefix + warc_dir + '/' + js, 'rb')
    chars = 0
    while True:
      line = f.readline()
      if not line: break
      chars += len(line)
    f.close()
    avg_l = (avg_l * avg_count + chars) / (avg_count + 1)
    avg_count += 1
    if chars > max_l:
      max_l = chars
      max_path = dir_prefix + warc_dir + '/' + js

if IS_BENIGN_JS_COUNTER:
  print("total benign js: " + str(js_count))
else:
  print("total malicious js: " + str(js_count))
print("max length: " + str(max_l) + '(' + max_path + ')')
print("avg length: " + str(avg_l))
