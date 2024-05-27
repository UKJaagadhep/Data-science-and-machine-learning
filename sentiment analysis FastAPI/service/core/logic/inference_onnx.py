from transformers import BertTokenizerFast
import numpy as np
import service.main as s

model_id = "microsoft/xtremedistil-l6-h256-uncased"
tokenizer = BertTokenizerFast.from_pretrained(model_id)

def sentiment_analyzer(text):

    inputs = tokenizer(text, padding = 'max_length', max_length = 512, truncation = True, return_tensors = "np")
    
    inputs = {key: value.astype(np.int64) for key, value in inputs.items()}
 
    onnx_pred = s.m.run(["logits"], {'input_ids' : inputs['input_ids'],
                                'token_type_ids' : inputs['token_type_ids'],
                                'attention_mask' : inputs['attention_mask']})

    if onnx_pred[0][0][1] > onnx_pred[0][0][0]:
        review = "positive"
    else:
        review = "negative"
        
    return {"emotion":review}
