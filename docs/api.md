# API

The main application API starts with `pipeline.pipeline.AnalysisPipeline`.

```python
from lexicon.dictionary import Dictionary
from pipeline.pipeline import AnalysisPipeline

result = AnalysisPipeline(Dictionary("data/dictionaries/basic.json")).run("धर्म कर्म।")
```
