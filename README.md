# home-depot-hackathon

A piece of garbage written by me and Jerry. this won 5th @ GATech + Home Depot's deep learning hackathon.
We're both honestly kinda surprised because this is our **first experience ever with deep learning.**

We ripped off a VGG implementation pretrained on FER2013 and CTK+, turned it into a flask server, and wrote a react frontend.
The VGG scans for facial expression features and returns weights on each expression. We used pearson's R on two sets of weights to see if two faces had similar expressions.

We should've done a lot of things differently (open_cv face detection and a *tiny* bit of feature engineering lol)
