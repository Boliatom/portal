import { useEffect, useRef, useState } from 'react';
import { useParams } from 'react-router-dom';

function loadScript(url, tag) {
  return new Promise((resolve, reject) => {
    if (customElements.get(tag)) {
      resolve();
      return;
    }
    const script = document.createElement('script');
    script.src = url;
    script.onload = resolve;
    script.onerror = () => reject(new Error('Не удалось загрузить модуль'));
    document.head.appendChild(script);
  });
}

export default function ModulePage({ modules }) {
  const { code } = useParams();
  const module = modules.find((m) => m.code === code);
  const box = useRef(null);
  const [error, setError] = useState('');

  useEffect(() => {
    setError('');
    box.current.replaceChildren();
    if (!module) {
      return;
    }
    loadScript(module.url, module.tag)
      .then(() => box.current.replaceChildren(document.createElement(module.tag)))
      .catch((err) => setError(err.message));
  }, [module?.id]);

  return (
    <div>
      {!module && <p>Модуль не найден</p>}
      {error && <p>{error}</p>}
      <div ref={box} />
    </div>
  );
}
