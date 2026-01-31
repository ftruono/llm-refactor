# llm-refactor
Definition and rules for a llm refactor - specific for AI code

AI Specific Code Smells

Pandas et simila

| Name                                   | Description                                                                               |
| -------------------------------------- | ----------------------------------------------------------------------------------------- |
| **Chain Indexing**                     | Chained indexing on DataFrames (e.g., `df["col"][0]`) causing inefficiency and ambiguity. |
| **DataFrame Conversion API Misused**   | Using `.values()` instead of `.to_numpy()` or `.array`.                                   |
| **Implicit Copy via Slice**            | Modifying slices without `.loc`, leading to `SettingWithCopyWarning`.                     |
| **Row-wise Iteration**                 | Using `iterrows()` instead of vectorized operations.                                      |
| **Apply Overuse**                      | Excessive use of `.apply()` where vectorization is possible.                              |
| **Inplace Mutation Abuse**             | Overuse of `inplace=True`, reducing readability and predictability.                       |
| **Hardcoded Column Names**             | Column names embedded directly in logic instead of configuration.                         |
| **Mixed Preprocessing Logic**          | Data cleaning mixed with feature engineering.                                             |
| **Implicit Type Casting**              | Relying on Pandas implicit dtype conversion.                                              |
| **Duplicate Train/Test Preprocessing** | Same preprocessing logic duplicated for train and test sets.                              |

Numpy

**| Name                                  | Description                                                 |
| ------------------------------------- | ----------------------------------------------------------- |
| **Matrix Multiplication API Misused** | Using `np.dot()` instead of `@` or `np.matmul()`.           |
| **Broadcasting Assumption**           | Implicit reliance on NumPy broadcasting without validation. |
| **Loop-based Tensor Ops**             | Python loops instead of vectorized NumPy operations.        |
| **Unnecessary Array Copy**            | Using `np.array()` instead of `np.asarray()`.               |
| **Implicit Shape Dependency**         | Logic depends on undocumented tensor shapes.                |
| **Mixed Precision Ignorance**         | No control over float32/float64 usage.                      |
| **Manual Normalization Logic**        | Custom normalization instead of library utilities.          |
**

PyTorch

| Name                            | Description                                           |
| ------------------------------- | ----------------------------------------------------- |
| **Gradients Not Cleared**       | Missing `optimizer.zero_grad()` before `backward()`.  |
| **PyTorch Call Method Misused** | Calling `self.net.forward()` instead of `self.net()`. |
| **Training Mode Not Set**       | Missing `model.train()` or `model.eval()`.            |
| **No Grad Context Misused**     | Missing `torch.no_grad()` during inference.           |
| **Tensor Device Mismatch**      | Mixing CPU and GPU tensors.                           |
| **Implicit Tensor Detach**      | Using `.data` instead of `.detach()`.                 |
| **Loss Accumulation Bug**       | Accumulating loss tensors instead of scalars.         |
| **Optimizer Inside Loop**       | Re-creating optimizer inside training loop.           |
| **Hardcoded Device Selection**  | Explicit `"cuda"` strings scattered in code.          |
| **Non-deterministic Training**  | Missing seed setup for reproducibility.               |

TensorFlow/Keras

| Name                           | Description                                                            |
| ------------------------------ | ---------------------------------------------------------------------- |
| **TensorArray Not Used**       | Using `tf.constant()` repeatedly in loops instead of `tf.TensorArray`. |
| **Eager-Only Training Logic**  | Training logic incompatible with graph mode.                           |
| **Manual Gradient Tape**       | Using `GradientTape` where `model.fit()` is appropriate.               |
| **Implicit Model Compilation** | Compilation parameters scattered across code.                          |
| **Mixed Keras and TF Ops**     | Mixing low-level TF ops inside Keras models.                           |
| **Callback Logic Duplication** | Repeated custom callbacks across experiments.                          |


In progress others

