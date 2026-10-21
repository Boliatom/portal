import { useEffect, useState } from 'react';
import { BrowserRouter, Link, Navigate, Route, Routes } from 'react-router-dom';
import { getMe, removeToken } from './api';
import Login from './Login';
import Home from './Home';
import Profile from './Profile';
import About from './About';

export default function App() {
  const [user, setUser] = useState(null);
  const [loaded, setLoaded] = useState(false);

  async function loadUser() {
    setUser(await getMe());
    setLoaded(true);
  }

  useEffect(() => {
    loadUser();
  }, []);

  function logout() {
    removeToken();
    setUser(null);
  }

  if (!loaded) {
    return null;
  }
  if (!user) {
    return <Login onLogin={loadUser} />;
  }
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Главная</Link> <Link to="/profile">Профиль</Link>{' '}
        <Link to="/about">О нас</Link> <button onClick={logout}>Выйти</button>
      </nav>
      <Routes>
        <Route path="/" element={<Home user={user} />} />
        <Route path="/profile" element={<Profile user={user} />} />
        <Route path="/about" element={<About />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  );
}
