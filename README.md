# llm-refactor
Definition and rules for a llm refactor - specific for AI code

AI Specific Code Smells

## Pandas et simila

| Name                                   | Description                                                                              | Refactoring                               |
| -------------------------------------- | ---------------------------------------------------------------------------------------- |-------------------------------------------|
| **Chain Indexing**                     | Chained indexing on DataFrames (e.g., `df["col"][0]`) causing inefficiency and ambiguity | Replace with .loc[], Extract Accessor     |
| **DataFrame Conversion API Misused**   | Using `.values()` instead of '.to_numpy()' or `.array`                                   | Replace API Call                          |
| **Implicit Copy via Slice**            | Modifying slices without `.loc`, leading to `SettingWithCopyWarning`                     | Replace with .loc[], Encapsulate Mutation |
| **Row-wise Iteration**                 | Using `iterrows()` instead of vectorized operations                                      | Vectorize Operation                       |
| **Apply Overuse**                      | Excessive use of `.apply()` where vectorization is possible                              | Replace with Vectorized API               |
| **Inplace Mutation Abuse**             | Overuse of `inplace=True`, reducing readability and predictability                       | Replace In-place with Assignment          |
| **Hardcoded Column Names**             | Column names embedded directly in logic instead of configuration                         | Introduce Configuration Object            |
| **Mixed Preprocessing Logic**          | Data cleaning mixed with feature engineering                                             | Extract Pipeline Stage                    |
| **Implicit Type Casting**              | Relying on Pandas implicit dtype conversion                                              | Introduce Explicit Casting                |
| **Duplicate Train/Test Preprocessing** | Same preprocessing logic duplicated for train and test sets                              | Extract Transformer                       |

## Numpy

| Name                                  | Description                                                 | Refactoring                               |
| ------------------------------------- | ----------------------------------------------------------- | ----------------------------------------- |
| **Matrix Multiplication API Misused** | Using `np.dot()` instead of `@` or `np.matmul()`            | tbd                                       |
| **Broadcasting Assumption**           | Implicit reliance on NumPy broadcasting without validation  | tbd                                       |
| **Loop-based Tensor Ops**             | Python loops instead of vectorized NumPy ops                | tbd                                       |
| **Unnecessary Array Copy**            | Using `np.array()` instead of `np.asarray()`                | tbd                                       |
| **Implicit Shape Dependency**         | Logic depends on undocumented tensor shapes                 | tbd                                       |
| **Mixed Precision Ignorance**         | No control over float32/float64 usage                       | tbd                                       |
| **Manual Normalization Logic**        | Custom normalization instead of library utilities           | tbd                                       |

## PyTorch

| Name                            | Description                                          | Refactoring           |
| ------------------------------- | ---------------------------------------------------- |-----------------------|
| **Gradients Not Cleared**       | Missing `optimizer.zero_grad()` before `backward()`  | tbd                   |
| **PyTorch Call Method Misused** | Calling `self.net.forward()` instead of `self.net()` | tbd                   |
| **Training Mode Not Set**       | Missing `model.train()` or `model.eval()`            | tbd                   |
| **No Grad Context Misused**     | Missing `torch.no_grad()` during inference           | tbd                   |
| **Tensor Device Mismatch**      | Mixing CPU and GPU tensors                           | tbd                   |
| **Implicit Tensor Detach**      | Using `.data` instead of `.detach()`                 | tbd                   |
| **Loss Accumulation Bug**       | Accumulating loss tensors instead of scalars         | tbd                   |
| **Optimizer Inside Loop**       | Re-creating optimizer inside training loop           | tbd                   |
| **Hardcoded Device Selection**  | Explicit `"cuda"` strings scattered in code          | tbd                   |
| **Non-deterministic Training**  | Missing seed setup for reproducibility               | tbd                   |

## TensorFlow/Keras

| Name                           | Description                                                           | Refactoring         |
| ------------------------------ | --------------------------------------------------------------------- |---------------------|
| **TensorArray Not Used**       | Using `tf.constant()` repeatedly in loops instead of `tf.TensorArray` | tbd                 |
| **Eager-Only Training Logic**  | Training logic incompatible with graph mode                           | tbd                 |
| **Manual Gradient Tape**       | Using `GradientTape` where `model.fit()` is appropriate               | tbd                 |
| **Implicit Model Compilation** | Compilation parameters scattered across code                          | tbd                 |
| **Mixed Keras and TF Ops**     | Mixing low-level TF ops inside Keras models                           | tbd                 |
| **Callback Logic Duplication** | Repeated custom callbacks across experiments                          | tbd                 |


Looking for others smells and example in code, not yet defined a specific prompt how to solve it!

