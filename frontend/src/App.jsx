import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [message, setMessage] = useState('Loading...')

  useEffect(() => {
    fetch('/api/hello/')
      .then((res) => res.json())
      .then((data) => setMessage(data.message))
      .catch(() => setMessage('Error fetching data'))
  }, [])

  return (
    <>
      <h1>{message}</h1>
      <p>
        Learn React at <a href="https://react.dev">react.dev</a>
      </p>
    </>
  )
}

export default App
