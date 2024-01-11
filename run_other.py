from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from tqdm import tqdm
import argparse
import os


# nllb language codes: https://github.com/facebookresearch/flores/tree/main/flores200#languages-in-flores-200
d = {
    'yo' : ('yor_Latn', 'Yoruba'),
    'ig' : ('ibo_Latn', 'Igbo'),
    'ar' : ('arz_Arab', 'Arabic'),
    'mg' : ('plt_Latn', 'Malagasy'),
    'sw' : ('swh_Latn', 'Swahili'),
    'en' : ('eng_Latn', 'English'),
}


def translate(args, text, tokenizer, model, src, tgt):
    if 'nllb' in args.model:
        inputs = tokenizer(text, return_tensors="pt", padding=True).to("cuda")
        translated_tokens = model.generate(
            **inputs, forced_bos_token_id=tokenizer.lang_code_to_id[d[tgt][0]], max_length=512
        )
        return tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
    elif 'mt0' in args.model:
        prompt = f"Translate from {d[src][1]} to {d[tgt][1]}: "
        inputs = tokenizer.encode(prompt + text, return_tensors="pt").to("cuda")
        outputs = model.generate(inputs, max_length=512)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    else:
        raise NotImplementedError

    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model')
    parser.add_argument('--src')
    parser.add_argument('--tgt')
    parser.add_argument('--output_dir')

    args = parser.parse_args()

    # Load Model
    model = AutoModelForSeq2SeqLM.from_pretrained(args.model, torch_dtype="auto").to("cuda")
    tokenizer = AutoTokenizer.from_pretrained(args.model)   
    if 'nllb' in args.model:
        tokenizer = AutoTokenizer.from_pretrained(args.model, src_lang=d[args.src][0])

    # Load Data
    if args.src == 'en':
        other = args.tgt
    else:
        other = args.src
    data_path = f'./data/eval/{other}en/test.{other}-en.{args.src}'
    with open(data_path, 'r') as f:
        data = f.readlines()
    
    translations = []
    print(f"Translating from {d[args.src][1]} to {d[args.tgt][1]}")
    for text in tqdm(data):
        translations.append(translate(args, text, tokenizer, model, args.src, args.tgt))
    
    output_path = f'{args.output_dir}/test-{args.src}-{args.tgt}'
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    with open(output_path, 'w') as f:
        for translation in translations:
            f.write(translation + '\n')
    print("Finished")
    
