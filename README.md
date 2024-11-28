# Steganography Example

This project demonstrates basic steganography techniques for hiding messages within images.

## Installation

1. Clone the repository:

   ```sh
   https://github.com/MysMon/steganography_example.git
   ```

2. Install dependencies using Poetry:

   ```sh
   poetry install
   ```

## Usage

1. **Encode a message into an image:**

   Use the image-embed script to embed a hidden message within an image.

   ```sh
   poetry run image-embed [input_image] [output_image] [text] [bits]
   ```

   **Example:**

   ```sh
   poetry run image-embed input.png output.png "Secret Message" 2
   ```

   This command will embed the text "Secret Message" into `input.png`, saving the result as `output.png` using 2 bits per color channel.

2. **Extract a message from an image:**

   Use the image-extract script to retrieve the hidden message from an image.

   ```sh
   poetry run image-extract [input_image] [bits]
   ```

   **Example:**

   ```sh
   poetry run image-extract output.png 2
   ```

   This command will extract the hidden text from `output.png` using 2 bits per color channel.

## License

This project is licensed under the MIT License.
