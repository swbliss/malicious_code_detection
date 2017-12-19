
f = open('devs/devs-2_2_model-0.7-0.05')

doc = ''

while True:
    line = f.readline()
    if not line: break
    doc += line + '\n'

l = doc.split('=')

res = []
for idx, content in enumerate(l):
    if idx%2 == 1:
        res.append(content[:14])

print(' '.join(res))
