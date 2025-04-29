use pyo3::prelude::*;
use rand::Rng;

#[pyclass]
pub struct AntiBotBypass {
    rng: rand::rngs::ThreadRng,
}

#[pymethods]
impl AntiBotBypass {
    #[new]
    fn new() -> Self {
        AntiBotBypass {
            rng: rand::thread_rng(),
        }
    }

    fn randomize_transaction(&mut self, tx: PyObject) -> PyResult<PyObject> {
        Python::with_gil(|py| {
            // Randomize gas price and timing
            let gas_price: u64 = tx.getattr(py, "gasPrice")?.extract(py)?;
            let new_gas_price = (gas_price as f64 * self.rng.gen_range(0.95..1.05)) as u64;
            tx.setattr(py, "gasPrice", new_gas_price)?;
            Ok(tx)
        })
    }
}
