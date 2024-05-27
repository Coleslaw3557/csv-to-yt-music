# YouTube Music CSV Importer

This script imports tracks from a CSV file into a YouTube Music playlist and adds them to your "Liked Music". It uses the `ytmusicapi` library to interact with YouTube Music.

## Features

- Create a new YouTube Music playlist from a CSV file.
- Add tracks to the created playlist.
- Add tracks to your "Liked Music".
- Retry logic for network requests.
- Configurable number of retries and timeout for network requests.
- Skip tracks that have already been added.

## Prerequisites

- Python 3.6+
- `ytmusicapi` library

## Installation

1. **Clone the repository**


3. **Install the required packages**:
```
pip install ytmusicapi
```

4. **Generate `headers_auth.json`**:
   - Follow the instructions in the [ytmusicapi documentation]([https://ytmusicapi.readthedocs.io/en/latest/setup.html#authenticated-requests](https://ytmusicapi.readthedocs.io/en/stable/)) to generate the `headers_auth.json` file.

## Usage

1. **Prepare your CSV file**:
   Ensure your CSV file (`your_file.csv`) looks like this:

```
Title,Album,Artist "Peaches en Regalia","Encores","Les Cris de Paris, Geoffroy Jourdain" "Edge of Seventeen","Crystal Visions...The Very Best of Stevie Nicks","Stevie Nicks"
```


2. **Run the script**:
```
python your_script.py your_file.csv "My Playlist Name" added_songs.json --retries 3 --timeout 10
```


   - `your_file.csv`: Path to your CSV file.
   - `"My Playlist Name"`: Name of the playlist to create.
   - `added_songs.json`: Path to the file to store added song IDs.
   - `--retries`: (Optional) Number of retries for network requests (default: 3).
   - `--timeout`: (Optional) Timeout for network requests in seconds (default: 10).

## Example

```
python your_script.py your_file.csv "My Favorite Songs" added_songs.json --retries 5 --timeout 15
```


## Logging

The script uses Python's `logging` module to provide detailed information about its progress and any issues encountered. Logs are printed to the console.

## Error Handling

The script includes retry logic for network requests and handles common errors gracefully. If a track cannot be added after the specified number of retries, it will be skipped, and an error message will be logged.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.




