# README

To prepare the files

```
python scripts/prepare_examples.py --data-dir /Users/ajukic/Desktop/examples/results --num-examples 5
(cd examples && for file in *.wav; do sox "$file" "n_$file" norm -3; done)
python scripts/prepare_spectrograms.py --data-dir ./demo/examples
python scripts/prepare_code.py --examples-dir ./demo/examples
```

Plase generated code between

```
<!-- Insert examples ⬇️ -->
<!-- Insert examples ⬆️ -->
```