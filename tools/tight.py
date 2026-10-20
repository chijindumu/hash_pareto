import json
d=json.load(open('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/flow/variants/u1/runs/hard20/final/metrics.json'))
ws={k.split('__corner:')[1]:v for k,v in d.items() if k.startswith('timing__setup__ws__corner:')}
wc=min(ws,key=ws.get)
p=20.0
need = p - ws[wc] + 0.5
print(wc, ws[wc], need)
