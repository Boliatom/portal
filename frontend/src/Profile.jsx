function formatDate(value) {
  return value ? new Date(value).toLocaleString('ru-RU') : 'нет';
}

export default function Profile({ user }) {
  return (
    <div>
      <h1>Профиль</h1>
      <p>Логин: {user.username}</p>
      <p>Фамилия: {user.last_name}</p>
      <p>Имя: {user.first_name}</p>
      <p>Отчество: {user.middle_name || 'нет'}</p>
      <p>Email: {user.email || 'нет'}</p>
      <p>Аккаунт создан: {formatDate(user.created_at)}</p>
      <p>Первый вход: {formatDate(user.first_login_at)}</p>
    </div>
  );
}
