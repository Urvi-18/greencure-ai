import numpy as np
import torch
from backend.model_utils import model

OUT = "model/model.onnx"
dummy = torch.randn(1, 3, 224, 224)

try:
    torch.onnx.export(model, dummy, OUT, input_names=["input"],
                      output_names=["logits"], opset_version=17, dynamo=False)
except Exception as e:
    print("First exporter failed, trying the default one:", e)
    torch.onnx.export(model, dummy, OUT, input_names=["input"],
                      output_names=["logits"])

import onnxruntime as ort
sess = ort.InferenceSession(OUT, providers=["CPUExecutionProvider"])

diffs, same = [], 0
for _ in range(5):
    x = torch.randn(1, 3, 224, 224)
    with torch.no_grad():
        a = model(x).numpy()
    b = sess.run(None, {"input": x.numpy()})[0]
    diffs.append(float(np.abs(a - b).max()))
    same += int(a.argmax() == b.argmax())

print("max abs diff:", max(diffs))
print("same top class:", same, "/ 5")