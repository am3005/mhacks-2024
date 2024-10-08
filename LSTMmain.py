import argparse 
import torch
from LSTMmodel import CharLSTM
from LSTMtrain import train
from LSTMpredict import predict
from LSTMdataset import char_to_idx, idx_to_char
import requests

url = "http://127.0.0.1:8000/speak/"

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
        torch.save(model.state_dict(), "char_level_model.pth")
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

        try:
            response = requests.post(url, json=result)

            # Check if the request was successful
            if response.status_code == 200:
                print("Successfully called FastAPI:", response.json())
            else:
                print("Failed to call FastAPI:", response.status_code, response.text)

        except requests.exceptions.RequestException as e:
            print("Error calling the FastAPI application:", e)

if __name__ == "__main__":
    main()
