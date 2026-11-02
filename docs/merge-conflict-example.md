# Merge conflict example

A static copy of the conflict used in the training, in case the live demo does not work.
The live version is pull request #17 (`demo/conflict-change` into `demo/conflict-base`), which is always in conflict.

## How it happens

Two branches change the same line of `fabric/silver_clean.Notebook/notebook-content.py`:

| Branch | Change |
| --- | --- |
| `demo/conflict-base` | Strip spaces from postcodes |
| `demo/conflict-change` | Trim postcodes before upper-casing |

When Git tries to combine them, it cannot choose, so it stops and marks the file.

## What Git writes into the file

```text
    .withColumn("customer_name", F.trim(F.col("customer_name")))
<<<<<<< HEAD
    .withColumn("postcode", F.upper(F.trim(F.col("postcode"))))
=======
    .withColumn("postcode", F.upper(F.regexp_replace(F.col("postcode"), " ", "")))
>>>>>>> demo/conflict-base
```

- `<<<<<<< HEAD` to `=======` is your branch's version
- `=======` to `>>>>>>>` is the other branch's version

## How to resolve it

Decide what the result should be, keeping both intentions, delete the three marker lines, then commit:

```text
    .withColumn("customer_name", F.trim(F.col("customer_name")))
    .withColumn("postcode", F.upper(F.regexp_replace(F.trim(F.col("postcode")), " ", "")))
```

On GitHub use **Resolve conflicts** on the pull request. Locally:

```shell
git switch <your-branch>
git merge main
# edit the file, remove the markers
git add fabric/silver_clean.Notebook/notebook-content.py
git commit
git push
```

Manual: [Resolving merge conflicts](https://githubtraining.github.io/training-manual/#/12b_resolving_merge_conflicts)
