import argparse
import numpy as np
import torch
from transformers import LlamaForCausalLM, LlamaTokenizer

def set_embeddings(model_args):

    model = LlamaForCausalLM.from_pretrained(model_args.model)

    embedding_size = model.get_input_embeddings().weight.shape[0]
    input_embeddings = torch.from_numpy(np.load(model_args.input_embeddings_dir))
    output_embeddings = torch.from_numpy(np.load(model_args.output_embeddings_dir))

    print(f"Llama Embedding size: {embedding_size}")
    print(f"Extended Embedding size: {input_embeddings.size()}")
    model.resize_token_embeddings(embedding_size + input_embeddings.size()[0])
    
    # Embedding initlization for additional tokens

    model.get_input_embeddings().weight.data[embedding_size:] = input_embeddings
    model.get_output_embeddings().weight.data[embedding_size:] = output_embeddings
    if model_args.save_path:
        model.save_pretrained(model_args.save_path)
        print(f"Model saved to {model_args.save_path}")
    if model_args.push_to_hub:
        model.push_to_hub(model_args.push_to_hub)
        print(f"Model saved to HF hub with name {model_args.push_to_hub}")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, help="Source model")
    parser.add_argument("--input_embeddings_dir", type=str, help="File path where numpy input embeddings stored")
    parser.add_argument("--output_embeddings_dir", type=str, help="File path where numpy output embeddings stored")
    parser.add_argument("--save_path", type=str, help="Save path")
    parser.add_argument("--push_to_hub", type=str, help="Push to hub model name")
    args = parser.parse_args()

    set_embeddings(args)
