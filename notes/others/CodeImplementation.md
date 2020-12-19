# Code implementation notes

### Dependency direction of `dlparse`

`dlparse.mono.asset` &rarr; `dlparse.model` &rarr; `dlparse.transformer` &rarr; `dlparse.export`

- **Always** import the master asset/entry classes (`dlparse.mono.asset.master`)
  from the model classes (`dlparse.model`). **Never** import it in the opposite direction.
