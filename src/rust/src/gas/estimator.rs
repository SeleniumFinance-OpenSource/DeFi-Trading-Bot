use pyo3::prelude::*;
use web3_rs::Web3;
use web3_rs::types::U256;

#[pyclass]
pub struct GasEstimator {
    web3: Web3<web3_rs::transports::Http>,
}

#[pymethods]
impl GasEstimator {
    #[new]
    fn new(rpc_url: String) -> PyResult<Self> {
        let transport = web3_rs::transports::Http::new(&rpc_url)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Invalid RPC URL: {}", e)))?;
        let web3 = Web3::new(transport);
        Ok(GasEstimator { web3 })
    }

    fn estimate_gas_price(&self) -> PyResult<U256> {
        // Fetch recent block gas prices (simplified)
        Ok(self.web3.eth().gas_price().unwrap_or(U256::from(20_000_000_000u64)))
    }
}
