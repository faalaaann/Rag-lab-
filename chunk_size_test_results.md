# RAG Chunk-Size Test Results

Date: 2026-11-23

PDF: `C:\Users\Farhan\Downloads\cloudops m3.pdf`

Question used for both runs:

> What is CI/CD?

## Test 1: Chunk size 200

- Chunk overlap: 40
- Extracted chunks: 306
- Result:

```text
A: Based on the provided context, the definition or explanation of what CI/CD is is not included. The context only lists headings/table of contents entries mentioning "CI/CD Pipeline Concepts", "Continuous Integration (CI)", and "Continuous Delivery (CD)".
```

- Failure: None.
- Warning: Hugging Face Hub unauthenticated-request warning. The embedding model loaded and indexing completed.

## Test 2: Chunk size 1000

- Chunk overlap: 150
- Extracted chunks: 62
- Result:

```text
A: Based on the provided context, **CI/CD** refers to the following concepts:

* **Continuous Integration (CI):** A software development practice where developers merge their code changes into a shared repository frequently (usually several times a day). Every merge automatically triggers a build and automated tests to discover integration problems early when they are small and cheap to fix.
* **Continuous Delivery (CD):** An extension of CI where, after the build and tests pass, the pipeline automatically prepares the software for release (packaging it, deploying it to a test or staging environment, and running further checks). This creates a release candidate that can be deployed to production at any time via a manual decision.
* **Continuous Deployment:** A practice that goes a step further than Continuous Delivery, where every change that passes all automated stages is automatically deployed to production without any human approval.
```

- Failure: None.
- Warning: Hugging Face Hub unauthenticated-request warning. The embedding model loaded and indexing completed.

## Conclusion

Both test runs completed successfully. With 200-character chunks, the top retrieved context lacked enough explanatory material and returned “not included.” With 1000-character chunks, the retrieved context contained definitions for CI, CD, and Continuous Deployment.
