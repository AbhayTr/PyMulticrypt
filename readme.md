# PyMulticrypt

Python Module for secure End-2-End encryption using the Multicrypt algorithm made by me.

## Concept behind MultiCrypt Algrorithm

So, take a number, say 77 as your message.
Then, take another number, say 739 as your key (In actual, this number will be of 256 bits).
Now, to get your encrypted message, just add your key to the actual message
i.e. 77 + 739 in this case = 816. So your encrypted message is now 816.

Now, encrypt your key i.e. 739 in this case using RSA Encryption (Asymmetric Encryption)
i.e. encrypt your key with the public key of the recipient, then append the encrypted key
at the end of your encrypted message with any seperator charecter between the encrypted message 
and the encrypted key.

Now this message is your final encrypyed message which can be transmitted safely to the
recipient.

Now when the recipient receives your encrypted message, then for decrypting that message first the
recipient will seperate the actual encrypted message and the encrypted key from the seperator charecter
which you used between the actual encrypted message and encrypted key at the time of encrypting the message
(In actual, the seperator charecter is fixed for everyone and is equal to "K"). Then the recipient will
decrypt the encrypted key using his/her private key which is mathematically linked to his/her public key.

Then the recipient gets the actual key i.e. 739 in this case. Then all he/she has to do is minus the actual key
from the actual encrypted message to get the actual message i.e. 816 - 739 in this case = 77 which is the actual message
which you wanted to send to the recipient.

This is highly secure as the encrypted message is safe from brute force attack. Also, no one can reverse engineer the
encryption algorithm to decrypt the message as the key required to do so is encrypted asymmetrically
(i.e. using RSA encryption algorithm) and everyone knows that RSA Encryption cannot be broken due to its public-private
key pair system.

Hence, MultiCrypt encrypiton is a hybrid encryption algorithm (i.e. involves both symmetric encryption algorithm (key encryption)
and asymmetric encryption (RSA encryption)) which is ideal for transmitting any kind of data securely using any kind of network protocol.

## Installation

Simply using PyPi: 

```
pip install pymulticrypt
```
## Usage

```python
from pyfractals import MandelBrot

MandelBrot(mode = "image/graph", optional_params)
```
