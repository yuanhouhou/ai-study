from transformers import AutoTokenizer

setence = "i love you"

tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")

token_ids = tokenizer(setence).input_ids
print(token_ids)

for token_id in token_ids:
    print(tokenizer.decode(token_id))