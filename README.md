Wrapper for `groovyc` Groovy compiler to be used in pre-commit.
Intended for Jenkins pipelines, so performs strange things like removing all imports.
Running `groovyc` is one of the simplest ways to check that the files do not contain
any outrageous syntax errors.

# How to use

Add the hook to your `.pre-commit-config.yaml`:

repos:
- repo: https://github.com/Artalus/pre-commit-groovyc
  rev: v0.1
  hooks:
  - id: groovyc
