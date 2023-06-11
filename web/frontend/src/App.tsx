import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { Login, Registration } from './utils'
import { Payment } from './api/index'

function App() {
  const [count, setCount] = useState(0)
  const [Username, setUsername] = useState("")
  const [payStatus, setPayStatus] = useState("false")

  function handleChange(e: React.ChangeEvent<HTMLInputElement>): void {
    setUsername(e.target.value);
  }

  async function handlePayment (): Promise<void> {
    const response = await Payment();
    setPayStatus(response);
  }

  return (
    <>
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <input type="text" value={Username} onChange={handleChange} />
        <button onClick={() => Login(Username)}>
          Login
        </button>
        <button onClick={() => Registration(Username)}>
          Registration
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <button onClick={() => handlePayment()}>
          Payment
      </button>
      <h1>{ payStatus }</h1>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
