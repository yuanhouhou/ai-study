from transformers import AutoTokenizer


colors = [
    '102;194;165',
    "252;141;98",
    "141;160;203",
    "231;138;195",
    "166;216;84",
    "255;217;47"
]

def show_tokens(sentence : str,name : str):
    "show the tokens each separated by color"
    tokenizer = AutoTokenizer.from_pretrained(name)

    token_ids = tokenizer(sentence).input_ids

    #extract vocabulary length
    print(f"vocab length: {len(tokenizer)}")

    # Print a colored list of the original tokenizer tokens.
    for idx, token in enumerate(tokenizer.convert_ids_to_tokens(token_ids)):
        r, g, b = colors[idx % len(colors)].split(';')
        print(
            f'\x1b[38;2;{r};{g};{b}m{token}\x1b[0m',
            end = ' '
        )

text = """
English and CAPITALIZATION
🎶鸟
show_tokens False None elif == >= else:
two tabs:" " Three tabs : "   "
12.0*50 = 600
"""
show_tokens(text,"bert-base-chinese")
print("----------")
show_tokens(text,"Xenova/gpt-4")
