import torch
from LSTMmodel import CharLSTM  # Make sure this is your model's definition
from LSTMdataset import char_to_idx, idx_to_char  # Ensure these are defined correctly

def decode_sequence(sequence, idx_to_char):
    """Convert a list of indices to a string using idx_to_char mapping."""
    return "".join([idx_to_char[idx] for idx in sequence])

def encode_sequence(sequence, char_to_idx):
    """Convert a string to a list of indices using char_to_idx mapping."""
    return [char_to_idx[char] for char in sequence]

def predict(model, input_seq, char_to_idx, idx_to_char):
    """Make predictions based on the input sequence."""
    model.eval()  # Set the model to evaluation mode
    encoded_input = torch.tensor(encode_sequence(input_seq, char_to_idx)).unsqueeze(0)  # Add batch dimension
    with torch.no_grad():  # Disable gradient calculation for inference
        output = model(encoded_input)
        predicted_indices = torch.argmax(output, dim=-1)  # Get the index of the highest score
        predicted_indices = predicted_indices.squeeze(0).tolist()  # Remove the batch dimension

    predicted_text = decode_sequence(predicted_indices, idx_to_char)  # Decode indices to characters
    return predicted_text

# Initialize model parameters
vocab_size = len(char_to_idx)
embedding_dim = 64
hidden_dim = 256

# Create the model instance and load the saved weights
model = CharLSTM(vocab_size, embedding_dim, hidden_dim)  # Initialize the model
model.load_state_dict(torch.load("char_level_model.pth", map_location=torch.device('cpu')))  # Load the saved state_dict
model.eval()  # Set the model to evaluation mode

# Define your test input
test_input = "GOBLUE"
predicted_output = predict(model, test_input, char_to_idx, idx_to_char)  # Call the predict function

# # Print the results
# print(f"Input: {test_input}")
# print(f"Predicted Output: {predicted_output}")
