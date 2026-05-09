# Instant-Point-to-Point-Messaging-Tool
Computer Security Final

This project implements a simple, secure messaging application that allows two users to exchange encrypted messages over a network. The goal is to demonstrate core security concepts such as key derivation, encryption, IV usage, and periodic key rotation, while also providing a functional graphical interface.

The system uses a client/server model built with Python sockets and includes a Tkinter-based GUI for sending and receiving messages.

## Features

### End-to-End Encryption
All messages are encrypted using AES-128 in CBC mode. AES was selected because it is a widely used, modern block cipher that exceeds the assignment requirement of a minimum 56-bit key.

### Password-Based Key Derivation
Users enter a shared password when launching the program.  
The password is not used directly as the encryption key.  
Instead, both sides derive the same key using PBKDF2, which strengthens the password and protects against brute-force attacks.

### Random IV for Every Message
Each message is encrypted with a fresh, random initialization vector.  
This ensures that sending the same plaintext multiple times results in different ciphertext, preventing pattern analysis.

### Periodic Key Updates
The system automatically updates the encryption key every 20 messages.  
Both sides maintain a shared message counter and derive a new key using PBKDF2 when the counter reaches the update threshold.  
This provides forward secrecy by limiting how long any single key is used.

### Graphical User Interface
The GUI displays:
- Sent plaintext  
- Sent ciphertext  
- Received ciphertext  
- Decrypted plaintext  

This makes it easy to observe how the encryption and decryption processes work.

### Simple Networking Model
The server listens for incoming connections, and the client connects using a standard TCP socket.  
A background thread handles incoming messages so the GUI remains responsive.

## Project Structure

secure_chat/
│── gui_client.py
│── gui_server.py
│── crypto_utils.py
│── bonus2_auth_utils.py
│── bonus2_gui_client.py
│── bonus2_gui_server.py
│── bob__public.pem
│── bob__private.pem
│── alice__public.pem
│── alice__private.pem
│── README.md

## File Organization
The secure_chat folder contains the main project files: gui_client.py, gui_server.py, and crypto_utils.py. These files implement the required secure messaging system with the GUI, encryption, key derivation, random IVs, and periodic key updates.

The bonus files are bonus2_gui_client.py, bonus2_gui_server.py, and bonus2_auth_utils.py. These are for the Bonus 2 extension, where Alice and Bob do not use a pre-shared password and instead authenticate each other and establish a shared session key using RSA. The included .pem files are demo RSA key files used for this bonus feature.

## Security Summary
This project demonstrates several important security mechanisms:

- AES-128 encryption for confidentiality  
- PBKDF2 for secure key derivation  
- Random IVs to prevent ciphertext repetition  
- Periodic key rotation for forward secrecy  
- Encrypted communication over a TCP socket

## Authors
Ruby Morales, Trinh Nhan, Ivan Fraire
