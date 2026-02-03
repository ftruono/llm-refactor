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

| Name                                  | Description                                                 | Refactoring                            |
| ------------------------------------- | ----------------------------------------------------------- | -------------------------------------- |
| **Matrix Multiplication API Misused** | Using `np.dot()` instead of `@` or `np.matmul()`            | Replace with `@` / `np.matmul()`       |
| **Broadcasting Assumption**           | Implicit reliance on NumPy broadcasting without validation  | Introduce Shape Assertion              |
| **Loop-based Tensor Ops**             | Python loops instead of vectorized NumPy ops                | Vectorize Computation                  |
| **Unnecessary Array Copy**            | Using `np.array()` instead of `np.asarray()`                | Replace with `np.asarray()`            |
| **Implicit Shape Dependency**         | Logic depends on undocumented tensor shapes                 | Introduce Shape Contract               |
| **Mixed Precision Ignorance**         | No control over float32/float64 usage                       | Introduce Precision Policy             |
| **Manual Normalization Logic**        | Custom normalization instead of library utilities           | Replace with Library Utility           |

## PyTorch

| Name                            | Description                                          | Refactoring                      |
| ------------------------------- | ---------------------------------------------------- |----------------------------------|
| **Gradients Not Cleared**       | Missing `optimizer.zero_grad()` before `backward()`  | Insert Gradient Reset            |
| **PyTorch Call Method Misused** | Calling `self.net.forward()` instead of `self.net()` | Replace with Callable Module     |
| **Training Mode Not Set**       | Missing `model.train()` or `model.eval()`            | Introduce Training State Handler |
| **No Grad Context Misused**     | Missing `torch.no_grad()` during inference           | Wrap Inference Context           |
| **Tensor Device Mismatch**      | Mixing CPU and GPU tensors                           | Introduce Device Abstraction     |
| **Implicit Tensor Detach**      | Using `.data` instead of `.detach()`                 | Replace with `.detach()`         |
| **Loss Accumulation Bug**       | Accumulating loss tensors instead of scalars         | Accumulate Scalars               |
| **Optimizer Inside Loop**       | Re-creating optimizer inside training loop           | Move Initialization              |
| **Hardcoded Device Selection**  | Explicit `"cuda"` strings scattered in code          | Introduce Environment Config     |
| **Non-deterministic Training**  | Missing seed setup for reproducibility               | Introduce Reproducibility Setup  |

## TensorFlow/Keras

| Name                           | Description                                                           | Refactoring                   |
| ------------------------------ | --------------------------------------------------------------------- |-------------------------------|
| **TensorArray Not Used**       | Using `tf.constant()` repeatedly in loops instead of `tf.TensorArray` | Replace with `tf.TensorArray` |
| **Eager-Only Training Logic**  | Training logic incompatible with graph mode                           | Extract Training Step         |
| **Manual Gradient Tape**       | Using `GradientTape` where `model.fit()` is appropriate               | Replace with `model.fit()`    |
| **Implicit Model Compilation** | Compilation parameters scattered across code                          | Centralize Compilation        |
| **Mixed Keras and TF Ops**     | Mixing low-level TF ops inside Keras models                           | Separate Layers from Ops      |
| **Callback Logic Duplication** | Repeated custom callbacks across experiments                          | Extract Callback Class        |


Looking for examples in code, not yet defined a specific prompt how to solve it!

