# Stotra Pathashala

A small web app for learning five stotras verse by verse, in Devanagari and Telugu, with meanings.

**Live:** https://balendus.github.io/StotraPathanam/

| Stotra | Source | Units |
|---|---|---|
| Sri Rudram (Namakam + Chamakam) | Krishna Yajur Veda, Taittiriya Samhita 4.5 and 4.7 | 73 sections |
| Guru Ashtakam | Adi Shankaracharya | 9 verses |
| Aditya Hrudayam | Valmiki Ramayana, Yuddha Kanda | 31 verses |
| Karthikeya (Subrahmanya) Bhujangam | Adi Shankaracharya | 33 verses |
| Shiva Stuti (Shambhu Stuti, recited by Shri Rama) | Brahma Purana, chapter 123 | 12 verses |

## Features

- Switch between Devanagari, Telugu, or both
- Meaning for every verse, plus key-word meanings for Guru Ashtakam, Aditya Hrudayam, Karthikeya Bhujangam and Shiva Stuti
- **Test recall** mode: blurs the verse except its first line; tap a line to check yourself
- Mark verses as *Learning* or *Memorised*, review the ones in progress, resume where you left off
- Adjustable text size, light and dark themes
- Progress is saved in your browser's local storage (per device)
- Installable: on iPhone, open the live link in Safari → Share → **Add to Home Screen**; on Android, Chrome menu → **Install app**. The icon is a tripundra (three lines of vibhuti) with a kumkum bindu, in `icons/`.

## Text

Sanskrit text is taken from [sanskritdocuments.org](https://sanskritdocuments.org) (ITRANS files in `build/`), converted to Devanagari and Telugu with [indic_transliteration](https://pypi.org/project/indic-transliteration/). A few encoding typos in the Rudram file were corrected (listed in `build/rudram.py`). Rudram is shown without svara (accent) marks; learn the chanting from a teacher or a trusted recording.

English meanings are original plain-language translations written for this app.

## Rebuilding

```bash
pip install indic_transliteration
cd build
python3 extract.py && python3 rudram.py && python3 build.py   # writes data.json
python3 - <<'EOF'
d=open('data.json').read().replace('</','<\\/')
t=open('../index.html').read()
import re
t=re.sub(r'(<script id="data" type="application/json">).*?(</script>)',lambda m:m.group(1)+d+m.group(2),t,flags=re.S)
open('../index.html','w').write(t)
EOF
```

To edit a meaning, change the matching entry in `build/m_*.py` and rebuild.
