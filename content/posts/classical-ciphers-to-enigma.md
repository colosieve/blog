+++
title = "Secret Codes"
subtitle = "From Ancient Spies to the Enigma Machine"
date = 2025-10-16T00:00:00Z
author = "colosieve"
layout = "slides"
tags = ["cryptography", "history", "ciphers", "encryption", "enigma"]
+++

## Why Keep Secrets?

<div style="display: flex; gap: 2rem; align-items: start;">
<div style="flex: 1;">

Throughout history, people needed to hide messages:

**Military commanders:**
- Battle plans
- Troop movements
- Secret strategies

**Spies and diplomats:**
- Intelligence reports
- Treaty negotiations
- Secret alliances

**Lovers:**
- Private letters
- Secret meetings

**The challenge:** How do you send a message that only your friend can read, even if your enemies intercept it?

**The solution:** **CIPHERS** - secret codes that scramble your message!

</div>
<div style="flex: 0 0 auto;">

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Letter_of_a_steward_-_3rd_century_B.C..JPG/300px-Letter_of_a_steward_-_3rd_century_B.C..JPG" alt="Ancient Greek papyrus letter" style="max-width: 400px;">

</div>
</div>

---

## Caesar Cipher (50 BCE)

<div style="display: flex; gap: 2rem; align-items: start;">
<div style="flex: 1;">

**Julius Caesar** used this cipher to send military messages to his generals.

**How it works:**
Shift each letter forward by a fixed number (usually 3).

**Example: Shift by 3**
```
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
D E F G H I J K L M N O P Q R S T U V W X Y Z A B C
```

**Encrypting "HELLO":**
- H → K
- E → H
- L → O
- L → O
- O → R

**Result:** KHOOR

**The weakness:** Only 25 possible shifts! Try them all in minutes.

</div>
<div style="flex: 0 0 auto;">

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Caesar3.svg/320px-Caesar3.svg.png" alt="Caesar Cipher wheel" style="max-width: 300px;">

</div>
</div>

---

## 🎮 Caesar Cipher Quiz #1

**Can you decode this message?**

```
DWWDFN DW GDZQ
```

<details>
<summary>Hint 1 (click to reveal)</summary>
Shift = 3 (same as Caesar used)

Remember: if the encrypted letter is D, shift BACKWARDS 3 to get A
</details>

<details>
<summary>Hint 2</summary>
First word: D→A, W→T, W→T, D→A, F→C, N→K
</details>

<details>
<summary>Answer</summary>
<strong>ATTACK AT DAWN</strong>

How to decrypt:
- D → A (shift back 3)
- W → T
- W → T
- D → A
- F → C
- N → K

- D → A
- W → T

- G → D
- D → A
- Z → W
- Q → N
</details>

---

## Atbash Cipher (600 BCE)

<div style="display: flex; gap: 2rem; align-items: start;">
<div style="flex: 1;">

**Ancient Hebrew cipher** - the oldest known substitution cipher!

**How it works:**
Reverse the alphabet: A↔Z, B↔Y, C↔X, etc.

**Encrypting "HELLO":**
- H → S
- E → V
- L → O
- L → O
- O → L

**Result:** SVOOL

**Fun fact:** Encrypting twice gives you back the original!
- HELLO → SVOOL → HELLO

</div>
<div style="flex: 0 0 auto;">

<div style="background: #f8f9fa; padding: 2rem; border-radius: 8px; border: 2px solid #0066cc;">
<div style="font-family: monospace; font-size: 0.95rem; line-height: 1.8;">
<div style="text-align: center; margin-bottom: 1rem; font-weight: bold; color: #0066cc;">Atbash Mapping</div>
<div style="margin-bottom: 0.5rem;">A B C D E F G H I J K L M</div>
<div style="margin-bottom: 1rem; color: #0066cc;">↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓</div>
<div style="margin-bottom: 1.5rem;">Z Y X W V U T S R Q P O N</div>
<div style="margin-bottom: 0.5rem;">N O P Q R S T U V W X Y Z</div>
<div style="margin-bottom: 1rem; color: #0066cc;">↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓</div>
<div>M L K J I H G F E D C B A</div>
</div>
</div>

</div>
</div>

---

## 🎮 Atbash Cipher Quiz #2

**Decode this secret message!**

```
HVXIVG NVHHZTV
```

<details>
<summary>Hint 1</summary>
Remember: A↔Z, B↔Y, C↔X, D↔W, E↔V...
</details>

<details>
<summary>Hint 2</summary>
H ↔ S, V ↔ E, X ↔ C...
</details>

<details>
<summary>Answer</summary>
<strong>SECRET MESSAGE</strong>

Decryption:
- H → S
- V → E
- X → C
- I → R
- V → E
- G → T

- N → M
- V → E
- H → S
- H → S
- Z → A
- T → G
- V → E
</details>

---

## General Substitution Cipher (Ancient - Modern)

<div style="display: flex; gap: 2rem; align-items: start;">
<div style="flex: 1;">

**Arbitrary letter substitution** - each letter maps to any other letter.

**Encrypting "HELLO":**
- H → I
- E → T
- L → S
- L → S
- O → G

**Result:** ITLLG

<details>
<summary>Click to reveal strength</summary>

**Strength:**
- 26! ≈ 403,291,461,126,605,635,584,000,000 possible keys!
- Can't try them all...
</details>

**But there's a weakness!** (We'll discover it on the next slide)

</div>
<div style="flex: 0 0 auto;">

<div style="background: #f8f9fa; padding: 2rem; border-radius: 8px; border: 2px solid #0066cc;">
<div style="font-family: monospace; font-size: 0.9rem; line-height: 2;">
<div style="text-align: center; margin-bottom: 1rem; font-weight: bold; color: #0066cc;">Example Substitution Key</div>
<div style="margin-bottom: 0.5rem; color: #666;">Plaintext alphabet:</div>
<div style="margin-bottom: 1.5rem; letter-spacing: 0.3em;">ABCDEFGHIJKLMNOPQRSTUVWXYZ</div>
<div style="margin-bottom: 0.5rem; color: #0066cc; font-weight: bold;">↓ Maps to ↓</div>
<div style="margin-bottom: 0.5rem; color: #666;">Cipher alphabet:</div>
<div style="letter-spacing: 0.3em;">QWERTYUIOPASDFGHJKLZXCVBNM</div>
</div>
</div>

</div>
</div>

---

## Breaking Substitution Ciphers: Frequency Analysis

<div style="display: flex; gap: 2rem; align-items: start;">
<div style="flex: 1;">

**The weakness:** English letters appear with predictable frequencies!

**Most common letters in English:**
1. **E** (12.7%) - The champion!
2. **T** (9.1%)
3. **A** (8.2%)
4. **O** (7.5%)
5. **I** (7.0%)
6. **N** (6.7%)

**How to break a substitution cipher:**
1. Count how often each cipher letter appears
2. Most common cipher letter is probably **E**
3. Look for common patterns:
   - **TH** (most common digraph)
   - **THE** (most common word)
   - **-ING** (common ending)

**Result:** Even with 26! possible keys, you can break it in minutes!

</div>
<div style="flex: 0 0 auto;">

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/English_letter_frequency_%28alphabetic%29.svg/400px-English_letter_frequency_%28alphabetic%29.svg.png" alt="Letter frequency" style="max-width: 400px;">

</div>
</div>

---

## 🎮 Frequency Analysis Quiz #3

**Use frequency analysis to crack this message!**

```
V ARIRE XRRC N FRPERG ZRFFNTR VA NA RAIRYBCR
```

<details>
<summary>Hint 1</summary>
Count the letters: Which appears most often? It's probably E!

The most common letter is "R" (appears 11 times). Try R → E:

```
_ _E_E_ _EE_ _ _E__E_ _E____E __ __ E__E___E
```
</details>

<details>
<summary>Hint 2</summary>
Single letters are usually "A" or "I". We have "V" and "N" appearing alone.

Try both options:

**Option 1:** V → I, N → A
```
I _E_E_ _EE_ A _E__E_ _E__A_E I_ A_ E__E___E
```

**Option 2:** V → A, N → I
```
A _E_E_ _EE_ I _E__E_ _E__I_E A_ I_ E__E___E
```

Which one makes more sense?
</details>

<details>
<summary>Hint 3</summary>
Option 1 makes more sense! "I" is a word, and "A_" looks like "AN".

If "A_" is "AN", then A → N. Let's add that:

```
I NE_E_ _EE_ A _E__E_ _E__A_E IN AN EN_E___E
```

Look at "NE_E_" - what 5-letter word starts with NE and has E in position 4?
</details>

<details>
<summary>Hint 4</summary>
Notice "_E__A_E" has double letters "_ _" in the middle.

Common double letters in English (most to least likely):
- **SS, EE, TT, FF, LL, MM, OO**
- **PP, RR, CC, DD, GG, NN, BB**
- Less common: ZZ, KK

We already know E, so it's not EE. What could "_ _" be?
</details>

<details>
<summary>Answer</summary>

**I NEVER KEEP A SECRET MESSAGE IN AN ENVELOPE**

This was encrypted using ROT13 (rotate by 13 positions).

</details>

---

## The Scytale: Ancient Transposition (400 BCE)

<div style="display: flex; gap: 2rem; align-items: start;">
<div style="flex: 1;">

**Spartan military cipher** - doesn't substitute letters, it **rearranges** them!

**How it works:**
1. Wrap a strip of parchment around a wooden rod (scytale)
2. Write your message DOWN the columns (vertically along the rod)
3. Unwrap the strip → letters are scrambled!
4. Receiver wraps on same-diameter rod, reads down to decrypt

**Example with 4-column rod:**
```
Message: ATTACKATDAWNSENDHELP

Wrap parchment and write DOWN each column:
A K W D
T A N H
T T S E
A D E L
C A N P

Unwrap strip and read left-to-right:
Encrypted: AKWDTANHTTSEADELCANP

Receiver wraps on matching 4-column rod:
A K W D
T A N H
T T S E
A D E L
C A N P

Reads DOWN columns: ATTACKATDAWNSENDHELP ✓
```

**The key:** The diameter of the rod (number of columns)!

**Weakness:** Only rearranges letters, doesn't hide their frequencies

</div>
<div style="flex: 0 0 auto;">

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Skytale.png/300px-Skytale.png" alt="Scytale" style="max-width: 300px;">

</div>
</div>

---

## 🎮 Scytale Activity #4

**Make your own Scytale!**

**What you need:**
- A pencil or pen (your "rod")
- A strip of paper (cut lengthwise, about 1 inch wide)
- Tape

**Instructions:**
1. Wrap the paper strip around your pencil (spiraling down)
2. Tape it so it doesn't unwrap
3. Write a secret message DOWN the length of the pencil
4. Unwrap the paper - your message is scrambled!
5. Give it to a friend with a matching pencil

**Try encrypting:** "MEET ME AFTER SCHOOL"

**Challenge:**
- Can you decrypt it with a thicker pen?
- What happens with a thinner pencil?
- The diameter is the key!

---

## Rail Fence Cipher: Zigzag Transposition

<div style="display: flex; gap: 2rem; align-items: start;">
<div style="flex: 1;">

**Another transposition cipher** - write in a zigzag pattern!

**How it works (3 rails):**

Write message in zigzag:
```
W . . . E . . . C . . . R . . . L . . . T . . . E
. E . R . D . S . O . E . E . F . E . A . O . C .
. . A . . . I . . . V . . . D . . . E . . . N . .
```

**Original message:** WE ARE DISCOVERED FLEE AT ONCE

**Read off each rail:**
- Rail 1: WECRLTE
- Rail 2: ERDSOEEFEAOC
- Rail 3: AIVDEN

**Encrypted:** WECRLTEERDSOEEFEAOCAIVDEN

**To decrypt:** Write in zigzag pattern again!

</div>
<div style="flex: 0 0 auto;">

<img src="https://www.101computing.net/wp/wp-content/uploads/rail-fence-cipher-encoding-key-3.png" alt="Rail fence cipher 3 rails" style="max-width: 400px;">

</div>
</div>

---

## 🎮 Rail Fence Activity #5

**Make your own Rail Fence Cipher with paper strips!**

**What you need:**
- 3 strips of paper (different colors if possible)
- Pencil and scissors

**How to do it:**

1. Cut 3 long paper strips and label them **Rail 1**, **Rail 2**, **Rail 3**

2. Write your message in zigzag across the 3 strips:
   ```
   Rail 1: M . . . T . . . I . . . I
   Rail 2: . E . A . M . D . I . H . T
   Rail 3: . . E . . . T . . . N . . . G
   ```

3. Read each rail left-to-right: **MTII** + **EAMDIHT** + **ENTG** = Encrypted!

4. Give the encrypted message to a friend - can they decrypt it?

**Challenge:** Try 2 rails (easier) or 4 rails (harder)!

---

## Alberti Cipher Disk (1467)

<div style="display: flex; gap: 2rem; align-items: start;">
<div style="flex: 1;">

**Leon Battista Alberti** invented the first **polyalphabetic cipher**!

**What's polyalphabetic?**
- Monoalphabetic: One substitution alphabet (Caesar, Atbash)
- **Polyalphabetic: Multiple alphabets** (changes during encryption!)

**How it works:**
- Two concentric disks with alphabets
- Outer disk (plaintext) fixed
- Inner disk (cipher) rotates
- Rotate the disk every few letters!

**Why it's revolutionary:**
- Same letter encrypts to different letters each time!
- 'A' might be 'D' first time, 'M' second time
- **Defeats frequency analysis!**

**This idea led to the Vigenère cipher...**

</div>
<div style="flex: 0 0 auto;">

<img src="https://upload.wikimedia.org/wikipedia/commons/2/23/Alberti_cipher_disk.svg" alt="Alberti cipher disk" style="max-width: 300px;">

</div>
</div>

---

## Vigenère Cipher (1553): "The Unbreakable Cipher"

<div style="display: flex; gap: 2rem; align-items: start;">
<div style="flex: 1;">

**Blaise de Vigenère** created a cipher that resisted breaking for **300 years**!

**How it works:**
Use a **keyword** to determine shifts (like multiple Caesar ciphers)

**Example - Keyword: "PASS"**
```
P = 15, A = 0, S = 18, S = 18 (A=0, B=1, C=2, ...)

Plaintext:  A T T A C K A T D A W N
Keyword:    P A S S P A S S P A S S
Shift by:   15 0 18 18 15 0 18 18 15 0 18 18
Ciphertext: P T L S R K S L S A O F
```

**Why it's strong:**
- 'A' encrypts to P, then R, then S (different each time!)
- Different keyword → completely different cipher
- **Defeated frequency analysis for 300 years!**

**The weakness:** The keyword **repeats**...

</div>
<div style="flex: 0 0 auto;">

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Vigen%C3%A8re_square_shading.svg/400px-Vigen%C3%A8re_square_shading.svg.png" alt="Vigenère square" style="max-width: 400px;">

</div>
</div>

---

## 🎮 Vigenère Cipher Quiz #6

<div style="display: flex; gap: 2rem; align-items: start;">
<div style="flex: 1;">

**Decrypt this message with keyword "DOG":**

```
KSYWWG
```

**Remember:** D = 3, O = 14, G = 6

**Hint:** Use the Vigenère square to help!

<details>
<summary>Answer</summary>
<strong>HESTIA</strong>

Decryption:
- K (10) - D (3) = H (7)
- S (18) - O (14) = E (4)
- Y (24) - G (6) = S (18)
- W (22) - D (3) = T (19)
- W (22) - O (14) = I (8)
- G (6) - G (6) = A (0)

**Result:** HESTIA (Greek goddess of the hearth and home)
</details>

</div>
<div style="flex: 0 0 auto;">

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Vigen%C3%A8re_square_shading.svg/400px-Vigen%C3%A8re_square_shading.svg.png" alt="Vigenère square" style="max-width: 400px;">

</div>
</div>

---

## Breaking Vigenère: Kasiski Examination (1863)

**For 300 years**, Vigenère was considered unbreakable...

**Then Friedrich Kasiski** noticed something:

**The keyword repeats!**

**If the plaintext has repeating patterns** (like "THE ... THE"), and they align with the same keyword letters, **the ciphertext repeats too!**

**Example:**
```
Plaintext:  THE FOX THE BOX
Keyword:    KEY KEY KEY KEY
Ciphertext: DLC PSV DLC LSV
            ^^^     ^^^
       Same plaintext + same keyword = same ciphertext!
```

**Kasiski's method:**
1. Find repeated sequences in ciphertext (DLC appears twice!)
2. Measure distance between them (8 letters apart)
3. Distance is likely a multiple of keyword length (8 ÷ ? )
4. Once you know keyword length, break into Caesar ciphers!

**Result:** Vigenère is broken!

---

## Playfair Cipher (1854)

**Charles Wheatstone** invented this, but **Lord Playfair** promoted it.

**Revolutionary idea:** Encrypt **pairs of letters** (digraphs) instead of single letters!

**How it works:**
1. Create 5×5 grid with keyword (I and J share a cell)
2. Break plaintext into pairs
3. Apply rules based on positions

**Example grid (keyword: MONARCHY):**
```
M O N A R
C H Y B D
E F G I/J K
L P Q S T
U V W X Z
```

**Rules:**
- **Same row:** Shift right: HE → YF
- **Same column:** Shift down: MU → CV
- **Rectangle:** Swap corners: HS → YM

**Used by:** British Army in Boer War, WWI

---

## 🎮 Playfair Cipher Exercise #7

**Using the MONARCHY grid, encrypt: "HI"**

```
M O N A R
C H Y B D
E F G I/J K
L P Q S T
U V W X Z
```

**Instructions:**
1. Find H and I in the grid
2. Determine which rule applies (same row, same column, or rectangle)
3. Apply the rectangle rule (swap corners)
4. Write down your encrypted result

---

## One-Time Pad: The ONLY Unbreakable Cipher (1882)

<div style="display: flex; gap: 2rem; align-items: start;">
<div style="flex: 1;">

**The perfect cipher** - proven mathematically unbreakable by **Claude Shannon** (1945)!

**How it works:**
1. Create a **truly random** key, same length as message
2. Use each key letter **exactly once** (never reuse!)
3. Add key to plaintext (mod 26)

**Example:**
```
Message: HELLO
Key:     XMCKL (truly random, never reused)
Cipher:  EQNVZ

H(7) + X(23) = 30 mod 26 = 4 = E
E(4) + M(12) = 16 = Q
L(11) + C(2) = 13 = N
L(11) + K(10) = 21 = V
O(14) + L(11) = 25 = Z
```

**Why it's unbreakable:**
- Every possible message is equally likely!
- No pattern to analyze
- Information-theoretically secure

**Why it's rarely used:**
- Key must be truly random (hard!)
- Key must be as long as message (impractical!)
- Key must never be reused (dangerous if violated!)
- Key distribution problem (how to share securely?)

</div>
<div style="flex: 0 0 auto;">

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/C.E._Shannon._Tekniska_museet_43069_%28cropped%29.jpg/300px-C.E._Shannon._Tekniska_museet_43069_%28cropped%29.jpg" alt="Claude Shannon" style="max-width: 300px;">

<p style="text-align: center; font-size: 0.9rem; color: #666; margin-top: 0.5rem;">Claude Shannon (1916-2001)</p>

</div>
</div>

---

## Code Books: A Different Approach (1700s - WWII)

<div style="display: flex; gap: 2rem; align-items: start;">
<div style="flex: 1;">

**Not a cipher** - replace entire words or phrases with code numbers!

**Example codebook:**
```
ATTACK          → 4729
RETREAT         → 8331
REINFORCEMENTS  → 2156
AT DAWN         → 7743
SEND            → 3891
```

**Message:** "SEND REINFORCEMENTS AT DAWN"

**Encoded:** 3891 2156 7743

**Advantages:**
- Very secure if codebook is secret
- Can't use frequency analysis on words
- Compact (numbers shorter than words)

**Disadvantages:**
- Codebook can be captured!
- Limited vocabulary
- Everyone needs same codebook
- Can't express new concepts not in book

**Famous example:** **Zimmermann Telegram** (WWI) - helped bring USA into war!

</div>
<div style="flex: 0 0 auto;">

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Cipher_No_9%2C_Union_Telegraphic_Cipher_Book%2C_c._1861-1862%2C_used_by_General_Joseph_Hooker_at_the_battle_of_Chancellorsville%2C_Virginia%2C_to_secure_messages_sent_by_telegraph_-_National_Cryptologic_Museum_-_DSC07713.JPG/300px-Cipher_No_9%2C_Union_Telegraphic_Cipher_Book%2C_c._1861-1862%2C_used_by_General_Joseph_Hooker_at_the_battle_of_Chancellorsville%2C_Virginia%2C_to_secure_messages_sent_by_telegraph_-_National_Cryptologic_Museum_-_DSC07713.JPG" alt="Union Telegraphic Cipher Book" style="max-width: 400px;">

</div>
</div>

---

## The Zimmermann Telegram (1917)

<div style="display: flex; gap: 2rem; align-items: start;">
<div style="flex: 1;">

**The code that changed World War I!**

**January 1917:** German Foreign Minister Arthur Zimmermann sent an encrypted telegram to Mexico:

**The secret proposal:**
- Germany would help Mexico reconquer Texas, New Mexico, and Arizona
- In exchange, Mexico would ally with Germany against the USA
- Promise: "Generous financial support"

**The British intercept and decrypt it!**

**The Room 40 codebreakers** (Britain's secret cryptanalysis team) had partially broken the German diplomatic code.

**March 1917:** Britain shares the decrypted telegram with the USA

**American public is outraged!**

**April 6, 1917:** USA declares war on Germany

**Result:** The telegram helped bring the USA into WWI, tipping the balance toward Allied victory.

</div>
<div style="flex: 0 0 auto;">

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/The_Zimmermann_Telegram.jpg/300px-The_Zimmermann_Telegram.jpg" alt="Zimmermann Telegram" style="max-width: 300px;">

</div>
</div>

---

## ADFGVX Cipher: WWI German Field Cipher (1918)

<div style="display: flex; gap: 2rem; align-items: start;">
<div style="flex: 1;">

**Combination of substitution + transposition** - two-stage encryption!

**Why "ADFGVX"?** These letters are very different in Morse code (less errors in transmission)

**Step 1: Fractionating Substitution**
Use 6×6 grid (includes digits):
```
    A D F G V X
  ┌─────────────
A │ 8 p 3 d 1 n
D │ l t 4 o a h
F │ 7 k b c 5 z
G │ j u 6 w g m
V │ x s v i r 2
X │ 9 e y 0 f q
```

**Each letter becomes a pair:**
- "ATTACK" → AT,TA,CK:
- A(row D, col G) → DG
- T(row D, col D) → DD
- T → DD
- A → DG
- C(row F, col G) → FG
- K(row F, col D) → FD

**Result:** DG DD DD DG FG FD

**Step 2: Columnar Transposition** (scramble the pairs with keyword)

**Very strong for its time!** Resisted Allied cryptanalysis for months.

</div>
</div>

---

## Breaking ADFGVX: Georges Painvin (1918)

<div style="display: flex; gap: 2rem; align-items: start;">
<div style="flex: 1;">

**French cryptanalyst Georges Painvin** broke ADFGVX in one of the greatest feats of cryptanalysis in history!

**The challenge:**
- Two-stage encryption (substitution + transposition)
- Germans changed keys frequently
- Painvin had to work from intercepted ciphertext only

**His breakthrough:**
- Noticed patterns in the fractionated pairs
- Used statistical analysis
- Worked backwards through both stages
- **Took months of exhausting work**

**June 1918:** Painvin broke the cipher during the German Spring Offensive

**The intelligence revealed:**
- German attack plans
- Troop movements
- Strategic positions

**Result:** Helped French forces repel the offensive, contributing to Allied victory

**The cost:** Painvin lost 33 pounds and had a nervous breakdown from the intense mental effort!

</div>
<div style="flex: 0 0 auto;">

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Paivin_Young_photo.jpg/250px-Paivin_Young_photo.jpg" alt="Georges Painvin" style="max-width: 300px;">

<p style="text-align: center; font-size: 0.9rem; color: #666; margin-top: 0.5rem;">Georges Painvin (1914)</p>

</div>
</div>

---

## Rotor Machines: Mechanical Encryption (1920s)

<div style="display: flex; gap: 2rem; align-items: start;">
<div style="flex: 1;">

**The next evolution:** Mechanical cipher machines with rotating wheels!

**How rotors work:**
- Each rotor is a substitution cipher (26 wires connecting letters)
- Rotors rotate with each keystroke
- Multiple rotors create polyalphabetic cipher
- **Millions of possible combinations!**

**Early rotor machines:**

**Hebern Rotor Machine (1917, USA)**
- First electric rotor machine
- Single rotor (not very secure)

**Kryha Machine (1920s, Germany)**
- Mechanical rotors
- Used by diplomatic services
- Broken by cryptanalysts

**These ideas led to the most famous cipher machine in history...**

**Coming next: The Enigma Machine!**

</div>
<div style="flex: 0 0 auto;">

<img src="https://upload.wikimedia.org/wikipedia/commons/1/1a/Hebern1.jpg" alt="Hebern rotor machine" style="max-width: 400px;">

</div>
</div>

---

## Summary: The Evolution of Ciphers

**Substitution Ciphers:**
- ✅ Caesar (50 BCE) - Simple shift → Brute force
- ✅ Atbash (600 BCE) - Reverse alphabet → Pattern recognition
- ✅ General substitution - Arbitrary mapping → **Frequency analysis**

**Defeating Frequency Analysis:**
- ✅ Alberti Disk (1467) - First polyalphabetic
- ✅ Vigenère (1553) - Keyword-based → **Kasiski examination**
- ✅ Playfair (1854) - Digraph encryption → Still vulnerable

**Transposition:**
- ✅ Scytale (400 BCE) - Physical wrapping
- ✅ Rail Fence - Zigzag pattern
- ✅ Columnar - Column-based rearrangement

**Hybrid Systems:**
- ✅ ADFGVX (1918) - Substitution + transposition → Statistical analysis

**The Unbreakable:**
- ✅ One-Time Pad - **Proven unbreakable!** (but impractical)

**Next:** Mechanical complexity → **The Enigma Machine!**

---

## What's Next: The Enigma Challenge

<div style="display: flex; gap: 2rem; align-items: start;">
<div style="flex: 1;">

**By the 1920s**, codebreakers had learned to crack every cipher through:
- Frequency analysis
- Pattern recognition
- Statistical methods
- Cribs (guessed plaintext)

**The Germans thought:** "What if we made a cipher so complex that even WITH these techniques, it would take years to break?"

**Enter: The Enigma Machine (1923)**
- Multiple rotors
- Plugboard scrambling
- Reflector (making encrypt = decrypt)
- **~10²³ possible settings per day**

**The challenge:**
Could anyone break a cipher with **quintillions** of possible keys?

**The hero:** A young British mathematician named **Alan Turing**...

**Next lesson:** How Turing and his team broke the "unbreakable" Enigma!

</div>
<div style="flex: 0 0 auto;">

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/EnigmaMachineLabeled.jpg/400px-EnigmaMachineLabeled.jpg" alt="Enigma machine" style="max-width: 400px;">

</div>
</div>

---

## References

**Classical Ciphers:**
- [Caesar Cipher - Wikipedia](https://en.wikipedia.org/wiki/Caesar_cipher)
- [Vigenère Cipher - Wikipedia](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher)
- [Playfair Cipher - Wikipedia](https://en.wikipedia.org/wiki/Playfair_cipher)
- [One-Time Pad - Wikipedia](https://en.wikipedia.org/wiki/One-time_pad)

**Historical Events:**
- [Zimmermann Telegram - Wikipedia](https://en.wikipedia.org/wiki/Zimmermann_Telegram)
- [ADFGVX Cipher - Wikipedia](https://en.wikipedia.org/wiki/ADFGVX_cipher)

**Cryptanalysis:**
- [Frequency Analysis - Wikipedia](https://en.wikipedia.org/wiki/Frequency_analysis)
- [Kasiski Examination - Wikipedia](https://en.wikipedia.org/wiki/Kasiski_examination)
