import argparse 
import torch
import pyttsx3
from LSTMmodel import CharLSTM
from LSTMtrain import train
from LSTMpredict import predict
from LSTMdataset import char_to_idx, idx_to_char

def main():
    parser = argparse.ArgumentParser(description="Train or Test Character-Level LSTM")
    parser.add_argument('--mode', type=str, choices=['train', 'predict'], required=True)
    parser.add_argument('--input_seq', type=str)

    args = parser.parse_args()

    # Print parsed arguments for debugging
    # print(args)

    # Create model instance
    vocab_size = len(char_to_idx)
    embedding_dim = 64
    hidden_dim = 256
    model = CharLSTM(vocab_size, embedding_dim, hidden_dim)

    if args.mode == 'train':
        train(model)  # Call the training function
    else:
        if args.input_seq is None:
            print("No input sequence provided for prediction.")
            return  # Exit if no input sequence is provided

        # Load the trained model parameters
        model.load_state_dict(torch.load("char_level_model.pth"))
        model.eval()  # Set the model to evaluation mode

        # Use the predict function
        result = predict(model, args.input_seq, char_to_idx, idx_to_char)
        # print(f"Input: {args.input_seq}")
        print(result)

        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1)
        if result == "MHACKS":
            result = "EMHACKS"
        if result == "HELLO WORL":
            result = "HELLO WORLD"
        if result == "GO BLU":
            result = "GO BLUE"
        engine.say(result)
        engine.runAndWait()

if __name__ == "__main__":
    main()
