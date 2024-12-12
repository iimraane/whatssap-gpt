# README: Automating WhatsApp with Selenium and OpenAI

## Description
This project automates the management of WhatsApp Web conversations by retrieving unread messages, generating contextual responses using OpenAI GPT, and sending those responses automatically. The script is designed to work in personal or professional environments that require automated interactions.

---

## Features
- Automatic connection to WhatsApp Web via Selenium.
- Detection of conversations with unread messages.
- Extraction of the last 10 to 20 messages with their authors and timestamps.
- Contextual response generation using OpenAI GPT.
- Sending responses directly in WhatsApp conversations.
- Automatic closing of discussions after sending the response.

---

## Prerequisites

### Required Software
1. **Python 3.x**: Ensure Python is installed on your system.
2. **Google Chrome**: Used as the browser for automation.
3. **ChromeDriver**: Must match your version of Google Chrome.

### Python Dependencies
Install the necessary libraries by running the following command:
```bash
pip install selenium openai
```

### OpenAI Configuration
1. Create an OpenAI account if you don't already have one.
2. Generate an OpenAI API key from your OpenAI dashboard.
3. Replace the `OPENAI_API_KEY` variable in the script with your API key.

---

## Usage

### Getting Started Steps
1. **Configure Chrome Profile**:
   - The script uses a Chrome user profile to maintain the session.
   - Update the `--user-data-dir` path in the script to match your environment.

2. **Run the Script**:
   Execute the script using the following command:
   ```bash
   python script_whatsapp.py
   ```

3. **Scan the QR Code**:
   Once WhatsApp Web is opened, scan the QR code to log in.

4. **Automation**:
   - The script detects unread conversations.
   - It retrieves recent messages, analyzes them, and generates a contextual response via OpenAI.
   - The response is sent automatically to the conversation.

---

## Workflow Structure

### Step 1: Connection
The script opens WhatsApp Web and waits for the user to scan the QR code to establish an active session.

### Step 2: Searching for Unread Chats
The script identifies conversations with unread messages using specific CSS or XPath selectors.

### Step 3: Retrieving Messages
- Incoming messages are extracted along with their authors and timestamps.
- The script limits retrieval to the last 10 to 20 messages for optimal contextual analysis.

### Step 4: Generating a Response
A message history is sent to OpenAI's GPT model to generate a response. The prompt includes instructions to make the response natural and contextually appropriate.

### Step 5: Sending the Response
The generated response is sent via WhatsApp Web using Selenium automation tools.

### Step 6: Closing the Discussion
After sending the response, the script closes the conversation to proceed to the next one.

---

## Limitations
1. **Dependence on WhatsApp Web**: The QR code must be scanned manually.
2. **Dynamic DOM Structure**: If WhatsApp changes its HTML structure, the script may require updates.
3. **Fixed Wait Times**: Pauses (`time.sleep`) may slow down execution.

---

## Possible Improvements
- Replace fixed pauses with explicit waits for better performance.
- Add robust error handling for cases where the DOM changes or network interruptions occur.
- Extend the script to handle multiple conversations simultaneously.

---

## Example Usage
1. Run the script:
   ```bash
   python script_whatsapp.py
   ```
2. Scan the QR code in the opened browser.
3. Observe the messages being automatically processed and responses being sent.

---

## Disclaimer
This project is designed for educational and experimental purposes. Using automation with WhatsApp may violate their terms of service. The author is not responsible for any consequences arising from its use.

---

## License

Please just don't steal my code...
