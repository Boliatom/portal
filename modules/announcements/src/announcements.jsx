import { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';

const API = 'http://localhost:8001/api/announcements';

function Announcements() {
  const [items, setItems] = useState([]);
  const [title, setTitle] = useState('');
  const [text, setText] = useState('');
  const [error, setError] = useState('');

  const load = async () => {
    setItems(await (await fetch(API)).json());
  };

  useEffect(() => {
    load();
  }, []);

  const add = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const me = await (await fetch('/api/check/', {
        headers: { Authorization: 'Bearer ' + localStorage.getItem('token') },
      })).json();
      const res = await fetch(API, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, text, author_id: me.user_id }),
      });
      if (!res.ok) {
        setError((await res.json()).error);
        return;
      }
      setTitle('');
      setText('');
      load();
    } catch {
      setError('Не удалось добавить объявление');
    }
  };

  const remove = async (id) => {
    await fetch(`${API}/${id}`, { method: 'DELETE' });
    load();
  };

  return (
    <div>
      <h1>Объявления</h1>
      <form onSubmit={add}>
        <input placeholder="Заголовок" value={title} onChange={(e) => setTitle(e.target.value)} />
        <input placeholder="Текст" value={text} onChange={(e) => setText(e.target.value)} />
        <button>Добавить</button>
      </form>
      <div>{error}</div>
      <ul>
        {items.map((a) => (
          <li key={a.id}>
            <b>{a.title}</b>
            <p>{a.text}</p>
            <small>{new Date(a.created_at).toLocaleString('ru-RU')}, автор: {a.author_id}</small>{' '}
            <button onClick={() => remove(a.id)}>Удалить</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

class AnnouncementsModule extends HTMLElement {
  connectedCallback() {
    createRoot(this).render(<Announcements />);
  }
}

customElements.define('announcements-module', AnnouncementsModule);
