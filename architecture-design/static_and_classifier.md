# Static vs Classifier ML

Not all AI-specific code smells require learning-based detection
To summarize the README.md list we can detect statically only 30% of them.

## Pandas 
| Smell                            |  Static Analysis  | Classifier  | Reasons                                  |
| -------------------------------- |:-----------------:|:-----------:|------------------------------------------|
| Chain Indexing                   |         ✅         |      ❌      | Pattern sintattico chiaro (`df["a"][0]`) |
| DataFrame Conversion API Misused |         ✅         |      ❌      | Chiamata API esplicita                   |
| Implicit Copy via Slice          |         ✅         |      ❌      | Pattern `.loc` assente                   |
| Row-wise Iteration               |         ✅         |      ❌      | Uso di `iterrows()`                      |
| Apply Overuse                    |        ⚠️         |      ✅      | Soglia dipendente dal contesto           |
| Inplace Mutation Abuse           |        ⚠️         |      ✅      | Richiede contesto d’uso                  |
| Hardcoded Column Names           |         ❌         |      ✅      | Richiede intent & generalizzazione       |
| Mixed Preprocessing Logic        |         ❌         |      ✅      | Smell architetturale                     |
| Implicit Type Casting            |        ⚠️         |      ✅      | Dipende dai dati                         |


## Numpy

| Smell                             | Static | Classifier | Reasons                              |
| --------------------------------- | :----: | :--------: |--------------------------------------|
| Matrix Multiplication API Misused |    ✅   |      ❌     | `np.dot()` vs `@`                    |
| Broadcasting Assumption           |    ❌   |      ✅     | based on shapes                      |
| Loop-based Tensor Ops             |   ⚠️   |      ✅     | based on dimension                   |
| Unnecessary Array Copy            |   ⚠️   |      ✅     | Context-dependent                    |
| Implicit Shape Dependency         |    ❌   |      ✅     | Semantic smell                       |
| Mixed Precision Ignorance         |    ❌   |      ✅     | not visible                          |
| Manual Normalization Logic        |   ⚠️   |      ✅     | Runtime detection - based on pattern |


## PyTorch

| Smell                       | Static | Classifier  | Reasons             |
| --------------------------- | :----: |:-----------:|---------------------|
| Gradients Not Cleared       |   ⚠️   |      ✅      | Dataflow cross-step |
| PyTorch Call Method Misused |    ✅   |      ❌      | .forward()          |
| Training Mode Not Set       |    ❌   |      ✅      | Cross-function      |
| No Grad Context Misused     |   ⚠️   |      ✅      | Based on context    |
| Tensor Device Mismatch      |    ❌   |      ✅      | Runtime-dependent   |
| Implicit Tensor Detach      |    ✅   |      ❌      | .data               |
| Loss Accumulation Bug       |    ❌   |      ✅      | semantic            |
| Optimizer Inside Loop       |   ⚠️   |      ✅      | Scope-sensitive     |
| Hardcoded Device Selection  |    ✅   |      ❌      | String literal      |
| Non-deterministic Training  |    ❌   |      ✅      | Global setup        |

## TensorFlow / Keras

| Smell                      | Static | Classifier | Motivazione       |
| -------------------------- | :----: | :--------: |-------------------|
| TensorArray Not Used       |   ⚠️   |      ✅     | Based on loop     |
| Eager-only Training Logic  |    ❌   |      ✅     | runtime           |
| Manual Gradient Tape       |   ⚠️   |      ✅     | Intention         |
| Implicit Model Compilation |    ❌   |      ✅     | Distributed       |
| Mixed Keras and TF Ops     |   ⚠️   |      ✅     | Context-Based     |
| Callback Logic Duplication |    ❌   |      ✅     | Based on semantic |


## Summarize

| Categoria | # Smells | Static | Classifier |
|-----------| -------- | ------ | ---------- |
| Pandas    | 10       | 4      | 6          |
| NumPy     | 7        | 2      | 5          |
| PyTorch   | 10       | 3      | 7          |
| TF/Keras  | 6        | 1      | 5          |
| **Total** | **33**   | **10** | **23**     |
