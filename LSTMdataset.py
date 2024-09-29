import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torch.nn.utils.rnn import pad_sequence
from collections import defaultdict

data = [
    ("MHAKCS", "MHACKS"),
    ("MHACSK", "MHACKS"),
    ("MHCAKS", "MHACKS"),
    ("MHACKS", "MHACKS"),
    ("MHAKCS", "MHACKS"),
    ("MHACSKS", "MHACKS"),
    ("MHACK", "MHACKS"),
    ("MHACSKS", "MHACKS"),
    ("MHAKC", "MHACKS"),
    ("MHACKSY", "MHACKS"),
    ("HELLOORLD", "HELLO WORLD"),
    ("HELLOWOLRD", "HELLO WORLD"),
    ("HELLO WORLD", "HELLO WORLD"),
    ("HELLOWORLD", "HELLO WORLD"),
    ("HELLOWORL", "HELLO WORLD"),
    ("HLELO WORLD", "HELLO WORLD"),
    ("HLOEL WORLD", "HELLO WORLD"),
    ("HELLOWROLD", "HELLO WORLD"),
    ("HELLO WRLD", "HELLO WORLD"),
    ("HELLO WROLD", "HELLO WORLD"),
    ("HELLO WOLD", "HELLO WORLD"),
    ("HLOOWORLD", "HELLO WORLD"),
    ("HELLOWRL", "HELLO WORLD"),
    ("HELLO WROLD", "HELLO WORLD"),
    ("HLLLO WORLD", "HELLO WORLD"),
    ("HLLLOORLD", "HELLO WORLD"),
    ("HELLOOWORLD", "HELLO WORLD"),
    ("HLELO WOLRD", "HELLO WORLD"),
    ("HELLOWORLD", "HELLO WORLD"),
    ("HLLWORLD", "HELLO WORLD"),
    ("HLLWRLD", "HELLO WORLD"),
    ("GO BULE", "GO BLUE"),
    ("GO BLU", "GO BLUE"),
    ("GO BLEW", "GO BLUE"),
    ("GO BULEE", "GO BLUE"),
    ("GOBLUE", "GO BLUE"),
    ("GO BLUEE", "GO BLUE"),
    ("GOBLUEE", "GO BLUE"),
    ("GO BLLUE", "GO BLUE"),
    ("GO BOLUE", "GO BLUE"),
    ("GO BLUUE", "GO BLUE"),
    ("GO BULED", "GO BLUE"),
    ("GOBU", "GO BLUE"),
    ("GOBLU", "GO BLUE"),
    ("GOBLUU", "GO BLUE"),
    ("GO BLAUE", "GO BLUE"),
    ("GOBLUW", "GO BLUE"),
    ("GO BLUES", "GO BLUE"),
    ("GO BLUU", "GO BLUE"),
]

vocab = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ '")
char_to_idx = {char: idx for idx, char in enumerate(sorted(vocab))}
idx_to_char = {idx: char for char, idx in char_to_idx.items()}
#print(f"Vocabulary size: {len(char_to_idx)}")

def encode_sequence(sequence, char_to_idx):
    encoded = []
    for char in sequence:
        if char in char_to_idx:
            encoded.append(char_to_idx[char])
        else:
            raise ValueError(f"Character '{char}' is not in the vocabulary.")
    return encoded

def get_dataset():
    encoded_inputs = []
    encoded_outputs = []

    for input_seq, output_seq in data:
        input_encoded = encode_sequence(input_seq, char_to_idx)
        output_encoded = encode_sequence(output_seq, char_to_idx)

        while len(output_encoded) < len(input_encoded):
            output_encoded.append(char_to_idx[' '])

        max_length = max(len(input_encoded), len(output_encoded))
        input_encoded = input_encoded + [0] * (max_length - len(input_encoded))
        output_encoded = output_encoded + [0] * (max_length - len(output_encoded))

        encoded_inputs.append(torch.tensor(input_encoded))
        encoded_outputs.append(torch.tensor(output_encoded))
    
    print(f"Input sequence length: {len(input_encoded)}, Output sequence length: {len(output_encoded)}")

    padded_inputs = pad_sequence(encoded_inputs, batch_first=True, padding_value=char_to_idx[' '])
    padded_outputs = pad_sequence(encoded_outputs, batch_first=True, padding_value=char_to_idx[' '])

    print(f"Padded inputs shape: {padded_inputs.shape}")
    print(f"Padded outputs shape: {padded_outputs.shape}")

    return padded_inputs.long(), padded_outputs.long()

if __name__ == "__main__":
    inputs, outputs = get_dataset()
    print(f"Sample encoded input: {inputs[0]}")
    print(f"Sample encoded output: {outputs[0]}")
   # print(f"Vocabulary: {char_to_idx}")
