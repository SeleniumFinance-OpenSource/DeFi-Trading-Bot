use pyo3::prelude::*;
mod transaction;
mod gas;
mod anti_bot;

#[pymodule]
fn pyo3_defi_selenium_bot(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<transaction::signer::TransactionSigner>()?;
    m.add_class::<transaction::builder::TransactionBuilder>()?;
    m.add_class::<gas::estimator::GasEstimator>()?;
    m.add_class::<anti_bot::bypass::AntiBotBypass>()?;
    Ok(())
}
