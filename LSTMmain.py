import argparse
import torch
from LSTMmodel import CharLSTM
from LSTMtrain import train
from LSTMpredict import predict
from LSTMdataset import char_to_idx, idx_to_char

def main():
    parser = argparse.ArgumentParser(description="Train or Test Character-Level LSTM")
    parser.add_argument('--mode', type=str, choices=['train', 'predict'], required=True,
                        help="Mode: 'train' to train the model, 'predict' to make predictions.")
    parser.add_argument('--input_seq', type=str, help="Input sequence for prediction.")

    args = parser.parse_args()

    # Create model instance
    vocab_size = len(char_to_idx)
    embedding_dim = 64
    hidden_dim = 256
    model = CharLSTM(vocab_size, embedding_dim, hidden_dim)

    if args.mode == 'train':
        train(model)  # Call the training function
    else:
        if args.input_seq is None:
            return  # Exit if no input sequence is provided
        
        # Load the trained model parameters
        model.load_state_dict(torch.load("char_level_model.pth"))
        model.eval()  # Set the model to evaluation mode
        
        # Use the predict function
        result = predict(model, args.input_seq, char_to_idx, idx_to_char)
        print(f"Input: {args.input_seq}")
        print(f"Predicted Output: {result}")

if __name__ == "__main__":
    main()
