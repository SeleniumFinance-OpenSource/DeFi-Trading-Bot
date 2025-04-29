use pyo3::prelude::*;
use ethabi::{Contract, Function};
use serde_json::Value;

#[pyclass]
pub struct TransactionBuilder {
    contract: Contract,
}

#[pymethods]
impl TransactionBuilder {
    #[new]
    fn new(abi: String) -> PyResult<Self> {
        let contract = Contract::load(abi.as_bytes())
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Invalid ABI: {}", e)))?;
        Ok(TransactionBuilder { contract })
    }

    fn build_buy_transaction(&self, params: Value, caller: String, value: u64, gas: u64, gas_price: u64) -> PyResult<Vec<u8>> {
        let function = self.contract.function("swapExactETHForTokens")
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Function not found: {}", e)))?;
        
        // Simplified: Encode function call
        let data = function.encode_input(&[]).unwrap();
        Ok(data)
    }

    fn build_sell_transaction(&self, params: Value, caller: String, gas: u64, gas_price: u64) -> PyResult<Vec<u8>> {
        let function = self.contract.function("swapExactTokensForETH")
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Function not found: {}", e)))?;
        
        // Simplified: Encode function call
        let data = function.encode_input(&[]).unwrap();
        Ok(data)
    }
}
