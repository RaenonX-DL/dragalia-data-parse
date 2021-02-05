# Code Testing Notes

## Test Categories

There are a few types of tests to run in different situations.

The main purpose of categorizing the tests is to save the test running time.

### `slow`

#### Feature

The test is expected to be slow.

#### Run Case

These tests should **only** run right before committing the code and Github Actions for quality assurance.

### `holistic`

#### Feature

The test will loop through the data, performing a **holistic** check, therefore the test might be slow.

## Performing Tests

To run the marked tests and other unmarked tests, specify the test category as a flag.

For example, to run slow tests and other unmarked tests, run:

```bash
pytest --slow
```

------

Additionally, there is a flag `--all` for running all tests. To run all the tests, run:

```bash
pytest --all
```
