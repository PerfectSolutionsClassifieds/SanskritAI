# Object Model

`Word`, `Sloka`, `Sentence`, and `AnalysisResult` are plain data objects.
They should not perform translation, grammar analysis, dictionary lookup, or export.

Use services for behavior:

```python
service = AnalysisService(dictionary)
result = service.analyze(sloka_text)
```
