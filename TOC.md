# Digitalizzazione di audio analogico

## Fedeltà e filologia

## Digitalizzazione Manuale vs automatizzazione

### Centro di sonologia computazionale e suo Metodo di digitalizzazione, specializzazione su open reel tapes


# MPAI

## Struttura di uno standard MPAI e come implementarlo

## Gli standard

## MPAI-AIF e AIMs

## MPAI-CAE

### MPAI-CAE-ARP (è l'implementazione del metodo del CSC, cos'è un codec, cosa fa, quali sono i suoi moduli)


# Conformance testing (a che serve, con specifica ambiente di sviluppo (python, poetry, git, gitlab DEI))

## Tests e Test Driven Development

### Pytest (funzionamento/utlità, xdist per parallelizzare, json-report per scrivere il report richiesto, fixtures per eseguire funzione per ogni file)

## MPAI-CAE-ARP packager

### Bug e altri problemi pre-esistenti (moviepy vs ffmpeg, offset)

### Come verificare uguaglianza tra video (ffmpeg e psnr)

### Come verificare uguaglianza tra audio (fingerprinting con chromaprint, suo wrapper in python, open source software e mie contribuzioni, comunicare col mantainer)

### Pulizia/reformat del codice della libreria (principio DRY, docstrings, unit tests, compatiblità windows ma esecuzione docker)

## MPAI-CAE-ARP audio analyser

### Problemi pre-esistenti (uso alias di pydantic ambiguo, typos, video analyser usa : invece di . e workaround, in windows scipy.signal.correlate da overflow perche tipo di default per numpy è int32, test non funzionanti)

### Come verificare che l'offset scelto è abbastanza vicino a quello reale (formula fornita + ffprobe)

### Come verificare che i file siano wav (RF64 ma in realtà va bene wav, libreria filetype, magic numbers, MIME)

### Come verificare che la classificazione sia corretta (non necessario ma utile per capire che l'IA non da sempre stessi risultati, output utilizzati per gli altri test, recall, precision)

## Parallelizzare o no? confronto di velocità

## Libreria mpai-cae-arp (a cosa serve)

### Bug: aggiornamento pydantic (che ha portato a dover aggiornare i moduli)

### Bug: formatting sbagliato delle EditingList scritte su file

### Bug: test di AudioWave a singolo canale non funzionante -> fix di get_channel

### Aggiornamento delle librerie perchè cross-dependencies ora supportate (librosa, llvmlite, numpy)

### Aggiornamento a python 3.11


# Conclusioni

## Cosa manca come test (gli altri AIMs)

## Cosa si potrebbe fare per l'audio digitalization/restoration (audio enhancement in input o basato su irregolarità, risvolti sulla fedeltà)
